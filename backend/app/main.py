import time
import uuid
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.errors import AppException, ErrorResponsePayload, ErrorDetail
from app.db.base import Base
from app.db.session import engine
from app.api.v1.router import api_router
# Import models to ensure they are registered with Base.metadata
import app.models.todo


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables automatically on startup (compatible with SQLite & MySQL)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Sistem Todo List API",
    description="REST API Todo List berbasis FastAPI dengan UUID v7, MySQL/relational database, filtering, sorting, pagination, dan bulk generator 1.000 data acak.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_request_id_and_timing(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or f"req_{uuid.uuid4().hex[:16]}"
    request.state.request_id = request_id
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{duration * 1000:.2f}ms"
    return response


# Exception Handlers matching SRS Section 6.7
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    req_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": [d.model_dump() if hasattr(d, "model_dump") else d for d in exc.details],
                "request_id": req_id
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    req_id = getattr(request.state, "request_id", None)
    details = []
    for err in exc.errors():
        field_loc = ".".join(str(loc) for loc in err.get("loc", []) if loc not in ("body", "query"))
        msg = err.get("msg", "Input tidak valid.")
        details.append({"field": field_loc or "body", "reason": msg})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request tidak valid.",
                "details": details,
                "request_id": req_id
            }
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    req_id = getattr(request.state, "request_id", None)
    code_map = {
        400: "BAD_REQUEST",
        404: "TODO_NOT_FOUND",
        422: "VALIDATION_ERROR",
        429: "RATE_LIMITED",
        500: "INTERNAL_ERROR",
        503: "SERVICE_UNAVAILABLE"
    }
    code = code_map.get(exc.status_code, "ERROR")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code,
                "message": str(exc.detail),
                "details": [],
                "request_id": req_id
            }
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    req_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Terjadi kesalahan internal server.",
                "details": [],
                "request_id": req_id
            }
        }
    )


# Mount API V1 routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Mount Static Frontend (Vue 3 SPA build) if available
frontend_dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
if os.path.exists(frontend_dist_path):
    assets_dir = os.path.join(frontend_dist_path, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="static_assets")

    @app.get("/{full_path:path}", tags=["Frontend SPA"], include_in_schema=False)
    async def serve_spa(full_path: str):
        file_path = os.path.join(frontend_dist_path, full_path)
        if full_path and os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist_path, "index.html"))
else:
    @app.get("/", tags=["Root"])
    def root():
        return {
            "app": "Sistem Todo List API",
            "version": "1.0.0",
            "docs": "/docs",
            "api_v1": settings.API_V1_PREFIX
        }

