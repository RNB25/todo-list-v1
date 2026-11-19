from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from app.models.todo import TodoStatus, TodoPriority


def format_iso_utc(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    # Format as 2026-11-19T01:08:15.123Z
    iso = dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return iso


class TodoBase(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TodoCreate(TodoBase):
    title: str = Field(..., description="Judul todo (1-255 karakter setelah di-trim)")
    status: Optional[TodoStatus] = Field(default=TodoStatus.PENDING, description="Status todo")
    priority: Optional[TodoPriority] = Field(default=TodoPriority.MEDIUM, description="Prioritas todo")
    description: Optional[str] = Field(default=None, max_length=10000, description="Deskripsi todo opsional (maks 10.000 karakter)")

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Title harus bertipe string.")
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Title tidak boleh kosong atau hanya berisi spasi.")
        if len(trimmed) > 255:
            raise ValueError("Title maksimal 255 karakter.")
        return trimmed


class TodoUpdate(TodoBase):
    title: Optional[str] = Field(default=None, description="Judul todo (1-255 karakter setelah di-trim)")
    status: Optional[TodoStatus] = Field(default=None, description="Status todo")
    priority: Optional[TodoPriority] = Field(default=None, description="Prioritas todo")
    description: Optional[str] = Field(default=None, max_length=10000, description="Deskripsi todo")

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not isinstance(v, str):
            raise ValueError("Title harus bertipe string.")
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Title tidak boleh kosong atau hanya berisi spasi.")
        if len(trimmed) > 255:
            raise ValueError("Title maksimal 255 karakter.")
        return trimmed

    @model_validator(mode="after")
    def check_at_least_one_field(self):
        fields = [self.title, self.status, self.priority, self.description]
        if all(f is None for f in fields):
            raise ValueError("Body PATCH tidak boleh kosong. Sertakan setidaknya satu field yang diubah.")
        return self


class TodoItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    status: TodoStatus
    priority: TodoPriority
    description: Optional[str] = None
    created_at: str
    updated_at: str

    @classmethod
    def from_orm_model(cls, todo) -> "TodoItem":
        return cls(
            id=str(todo.id),
            title=todo.title,
            status=todo.status,
            priority=todo.priority,
            description=todo.description,
            created_at=format_iso_utc(todo.created_at),
            updated_at=format_iso_utc(todo.updated_at),
        )


class TodoSingleResponse(BaseModel):
    data: TodoItem


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int


class TodoListResponse(BaseModel):
    data: List[TodoItem]
    meta: PaginationMeta


class BulkRandomRequest(TodoBase):
    count: Optional[int] = Field(default=1000, ge=1, le=1000, description="Jumlah data acak yang ingin dibuat (1 - 1000)")


class BulkRandomData(BaseModel):
    requested_count: int
    created_count: int


class BulkRandomResponse(BaseModel):
    data: BulkRandomData
    message: str = "Bulk todo berhasil dibuat."
