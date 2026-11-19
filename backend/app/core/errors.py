from typing import Any, List, Optional
from fastapi import HTTPException, status
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    field: Optional[str] = None
    reason: str


class ErrorResponsePayload(BaseModel):
    code: str
    message: str
    details: List[ErrorDetail] = []
    request_id: Optional[str] = None


class ErrorResponse(BaseModel):
    error: ErrorResponsePayload


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[List[ErrorDetail]] = None
    ):
        super().__init__(status_code=status_code, detail=message)
        self.code = code
        self.message = message
        self.details = details or []


class NotFoundException(AppException):
    def __init__(self, message: str = "Todo tidak ditemukan.", details: Optional[List[ErrorDetail]] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="TODO_NOT_FOUND",
            message=message,
            details=details
        )


class ValidationException(AppException):
    def __init__(self, message: str = "Request tidak valid.", details: Optional[List[ErrorDetail]] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="VALIDATION_ERROR",
            message=message,
            details=details
        )


class BadRequestException(AppException):
    def __init__(self, message: str = "Format request tidak dapat diproses.", details: Optional[List[ErrorDetail]] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="BAD_REQUEST",
            message=message,
            details=details
        )


class ServiceUnavailableException(AppException):
    def __init__(self, message: str = "Database atau dependensi utama tidak tersedia.", details: Optional[List[ErrorDetail]] = None):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            code="SERVICE_UNAVAILABLE",
            message=message,
            details=details
        )
