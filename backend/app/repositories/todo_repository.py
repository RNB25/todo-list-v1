import math
from datetime import datetime
from typing import Optional, List, Tuple
from sqlalchemy import select, func, or_, and_, desc, asc
from sqlalchemy.orm import Session
from app.models.todo import Todo, TodoStatus, TodoPriority
from app.core.errors import ValidationException


SORT_ALLOWLIST = {
    "created_at": Todo.created_at,
    "updated_at": Todo.updated_at,
    "title": Todo.title,
    "status": Todo.status,
    "priority": Todo.priority
}


class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, todo_id: str) -> Optional[Todo]:
        stmt = select(Todo).where(Todo.id == todo_id)
        return self.db.scalar(stmt)

    def create(self, todo: Todo) -> Todo:
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def bulk_create(self, todos: List[Todo]) -> int:
        try:
            self.db.add_all(todos)
            self.db.commit()
            return len(todos)
        except Exception:
            self.db.rollback()
            raise

    def update(self, todo: Todo) -> Todo:
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def delete(self, todo: Todo) -> None:
        self.db.delete(todo)
        self.db.commit()

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
    ) -> Tuple[List[Todo], int, int]:
        query = select(Todo)
        count_query = select(func.count(Todo.id))
        filters = []

        if status:
            filters.append(Todo.status == status)

        if priority:
            filters.append(Todo.priority == priority)

        if q:
            term = f"%{q.strip()}%"
            filters.append(
                or_(
                    Todo.title.ilike(term),
                    Todo.description.ilike(term)
                )
            )

        if created_from:
            filters.append(Todo.created_at >= created_from)

        if created_to:
            filters.append(Todo.created_at <= created_to)

        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))

        total_items = self.db.scalar(count_query) or 0
        total_pages = math.ceil(total_items / page_size) if total_items > 0 else 0

        # Validate sort column
        if sort_by not in SORT_ALLOWLIST:
            raise ValidationException(
                f"Kolom sort '{sort_by}' tidak diizinkan. Pilihan yang valid: {', '.join(SORT_ALLOWLIST.keys())}."
            )

        sort_col = SORT_ALLOWLIST[sort_by]
        if sort_order.lower() == "desc":
            query = query.order_by(desc(sort_col), desc(Todo.id))
        else:
            query = query.order_by(asc(sort_col), asc(Todo.id))

        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        todos = self.db.scalars(query).all()
        return todos, total_items, total_pages
