from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, status, Query, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoSingleResponse,
    TodoListResponse,
    BulkRandomRequest,
    BulkRandomResponse
)
from app.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post(
    "",
    response_model=TodoSingleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create single todo"
)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    service = TodoService(db)
    todo = service.create_todo(payload)
    return TodoSingleResponse(data=todo)


@router.get(
    "",
    response_model=TodoListResponse,
    status_code=status.HTTP_200_OK,
    summary="List todos with filters, sorting, and pagination"
)
def list_todos(
    status: Optional[str] = Query(None, description="Filter status: pending, progress, done"),
    priority: Optional[str] = Query(None, description="Filter priority: low, medium, high"),
    q: Optional[str] = Query(None, description="Pencarian substring pada title dan description"),
    created_from: Optional[datetime] = Query(None, description="Filter created_at >= nilai ini (ISO 8601)"),
    created_to: Optional[datetime] = Query(None, description="Filter created_at <= nilai ini (ISO 8601)"),
    sort_by: str = Query("created_at", description="Kolom urutan: created_at, updated_at, title, status, priority"),
    sort_order: str = Query("desc", description="Arah urutan: asc atau desc"),
    page: int = Query(1, ge=0, description="Nomor halaman (minimal 1)"),
    page_size: int = Query(20, ge=0, description="Jumlah item per halaman (1-100)"),
    db: Session = Depends(get_db)
):
    service = TodoService(db)
    return service.list_todos(
        status=status,
        priority=priority,
        q=q,
        created_from=created_from,
        created_to=created_to,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )


@router.post(
    "/bulk-random",
    response_model=BulkRandomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate 1.000 todo acak secara atomik"
)
@router.post(
    "/bulk",
    response_model=BulkRandomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate 1.000 todo acak secara atomik (alias)",
    include_in_schema=False
)
def bulk_random(
    payload: Optional[BulkRandomRequest] = None,
    db: Session = Depends(get_db)
):
    count = payload.count if payload and payload.count is not None else 1000
    service = TodoService(db)
    return service.bulk_generate_random(count)


@router.get(
    "/{id}",
    response_model=TodoSingleResponse,
    status_code=status.HTTP_200_OK,
    summary="Detail satu todo berdasarkan UUID v7"
)
def get_todo(id: str, db: Session = Depends(get_db)):
    service = TodoService(db)
    todo = service.get_todo_by_id(id)
    return TodoSingleResponse(data=todo)


@router.patch(
    "/{id}",
    response_model=TodoSingleResponse,
    status_code=status.HTTP_200_OK,
    summary="Update parsial satu todo"
)
def update_todo(id: str, payload: TodoUpdate, db: Session = Depends(get_db)):
    service = TodoService(db)
    todo = service.update_todo(id, payload)
    return TodoSingleResponse(data=todo)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Hapus satu todo berdasarkan UUID v7"
)
def delete_todo(id: str, db: Session = Depends(get_db)):
    service = TodoService(db)
    service.delete_todo(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
