import random
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
import uuid6

from app.models.todo import Todo, TodoStatus, TodoPriority, utc_now
from app.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoItem,
    TodoListResponse,
    PaginationMeta,
    BulkRandomResponse,
    BulkRandomData
)
from app.repositories.todo_repository import TodoRepository, SORT_ALLOWLIST
from app.core.errors import (
    NotFoundException,
    ValidationException,
    ErrorDetail
)


SAMPLE_VERBS = [
    "Selesaikan", "Perbaiki", "Review", "Implementasikan", "Rancang",
    "Optimasi", "Uji coba", "Perbarui", "Dokumentasikan", "Analisis",
    "Setup", "Deploy", "Integrasikan", "Refactor", "Monitoring"
]

SAMPLE_SUBJECTS = [
    "endpoint REST API", "skema database MySQL", "tampilan antarmuka Vue 3",
    "pipeline CI/CD GitHub Actions", "indeks pencarian performa tinggi",
    "autentikasi JWT dan sesi pengguna", "komponen modal konfirmasi",
    "dokumentasi spesifikasi SRS", "fitur pagination dan sorting",
    "pengujian otomatis pytest dan vitest", "desain responsif mobile",
    "penanganan error terstruktur", "koneksi pool database",
    "manajemen state pinia / composable", "audit aksesibilitas WCAG"
]

SAMPLE_PROJECTS = [
    "Sprint 1", "Core System", "Frontend Revamp", "Security Audit",
    "Performance Tuning", "Database Migration", "Release v1.0", "Internal Tools"
]


def validate_uuid(uuid_str: str) -> None:
    try:
        val = UUID(uuid_str)
        if str(val) != uuid_str.lower():
            raise ValueError()
    except (ValueError, AttributeError, TypeError):
        raise ValidationException(
            message="Format UUID tidak valid.",
            details=[ErrorDetail(field="id", reason=f"'{uuid_str}' bukan format string UUID v7 yang valid.")]
        )


class TodoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TodoRepository(db)

    def create_todo(self, payload: TodoCreate) -> TodoItem:
        todo_id = str(uuid6.uuid7())
        now = utc_now()

        todo = Todo(
            id=todo_id,
            title=payload.title,
            status=payload.status or TodoStatus.PENDING,
            priority=payload.priority or TodoPriority.MEDIUM,
            description=payload.description,
            created_at=now,
            updated_at=now
        )
        saved = self.repo.create(todo)
        return TodoItem.from_orm_model(saved)

    def get_todo_by_id(self, todo_id: str) -> TodoItem:
        validate_uuid(todo_id)
        todo = self.repo.get_by_id(todo_id)
        if not todo:
            raise NotFoundException(
                message="Todo tidak ditemukan.",
                details=[ErrorDetail(field="id", reason=f"Todo dengan ID '{todo_id}' tidak ditemukan.")]
            )
        return TodoItem.from_orm_model(todo)

    def update_todo(self, todo_id: str, payload: TodoUpdate) -> TodoItem:
        validate_uuid(todo_id)
        todo = self.repo.get_by_id(todo_id)
        if not todo:
            raise NotFoundException(
                message="Todo tidak ditemukan.",
                details=[ErrorDetail(field="id", reason=f"Todo dengan ID '{todo_id}' tidak ditemukan.")]
            )

        if payload.title is not None:
            todo.title = payload.title
        if payload.status is not None:
            todo.status = payload.status
        if payload.priority is not None:
            todo.priority = payload.priority
        if payload.description is not None:
            todo.description = payload.description

        todo.updated_at = utc_now()
        updated = self.repo.update(todo)
        return TodoItem.from_orm_model(updated)

    def delete_todo(self, todo_id: str) -> None:
        validate_uuid(todo_id)
        todo = self.repo.get_by_id(todo_id)
        if not todo:
            raise NotFoundException(
                message="Todo tidak ditemukan.",
                details=[ErrorDetail(field="id", reason=f"Todo dengan ID '{todo_id}' tidak ditemukan.")]
            )
        self.repo.delete(todo)

    def list_todos(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        q: Optional[str] = None,
        created_from: Optional[datetime] = None,
        created_to: Optional[datetime] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        page: int = 1,
        page_size: int = 20
    ) -> TodoListResponse:
        # Validations
        if status:
            valid_statuses = [e.value for e in TodoStatus]
            if status not in valid_statuses:
                raise ValidationException(
                    message="Parameter status tidak valid.",
                    details=[ErrorDetail(field="status", reason=f"Nilai harus salah satu dari: {', '.join(valid_statuses)}")]
                )

        if priority:
            valid_priorities = [e.value for e in TodoPriority]
            if priority not in valid_priorities:
                raise ValidationException(
                    message="Parameter priority tidak valid.",
                    details=[ErrorDetail(field="priority", reason=f"Nilai harus salah satu dari: {', '.join(valid_priorities)}")]
                )

        if created_from and created_to and created_from > created_to:
            raise ValidationException(
                message="Rentang tanggal created_at tidak valid.",
                details=[ErrorDetail(field="created_from", reason="created_from tidak boleh lebih besar daripada created_to.")]
            )

        if sort_by not in SORT_ALLOWLIST:
            raise ValidationException(
                message="Parameter sort_by tidak diizinkan.",
                details=[ErrorDetail(field="sort_by", reason=f"Pilihan yang valid: {', '.join(SORT_ALLOWLIST.keys())}")]
            )

        if sort_order.lower() not in ["asc", "desc"]:
            raise ValidationException(
                message="Parameter sort_order tidak valid.",
                details=[ErrorDetail(field="sort_order", reason="Nilai harus 'asc' atau 'desc'.")]
            )

        if page < 1:
            raise ValidationException(
                message="Parameter page minimal 1.",
                details=[ErrorDetail(field="page", reason="Page harus lebih besar dari atau sama dengan 1.")]
            )

        if page_size < 1 or page_size > 100:
            raise ValidationException(
                message="Parameter page_size di luar batas.",
                details=[ErrorDetail(field="page_size", reason="Page size harus bernilai antara 1 dan 100.")]
            )

        todos, total_items, total_pages = self.repo.list_todos(
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

        items = [TodoItem.from_orm_model(t) for t in todos]
        meta = PaginationMeta(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages
        )
        return TodoListResponse(data=items, meta=meta)

    def bulk_generate_random(self, count: int = 1000) -> BulkRandomResponse:
        if count < 1 or count > 1000:
            raise ValidationException(
                message="Jumlah bulk acak di luar rentang.",
                details=[ErrorDetail(field="count", reason="Count harus bernilai antara 1 sampai 1000.")]
            )

        statuses = list(TodoStatus)
        priorities = list(TodoPriority)

        todos_to_create = []
        now = utc_now()

        for i in range(count):
            verb = random.choice(SAMPLE_VERBS)
            subject = random.choice(SAMPLE_SUBJECTS)
            proj = random.choice(SAMPLE_PROJECTS)
            title = f"{verb} {subject} [{proj} #{random.randint(100, 999)}]"

            status_val = random.choice(statuses)
            priority_val = random.choice(priorities)
            description = (
                f"Deskripsi tugas otomatis: {title}. "
                f"Dibuat secara massal untuk pengujian beban dan verifikasi pagination."
            ) if random.random() > 0.15 else None

            todo = Todo(
                id=str(uuid6.uuid7()),
                title=title,
                status=status_val,
                priority=priority_val,
                description=description,
                created_at=now,
                updated_at=now
            )
            todos_to_create.append(todo)

        created_count = self.repo.bulk_create(todos_to_create)
        return BulkRandomResponse(
            data=BulkRandomData(
                requested_count=count,
                created_count=created_count
            ),
            message="Bulk todo berhasil dibuat."
        )
