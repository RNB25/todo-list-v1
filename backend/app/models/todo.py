import enum
from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Enum as SQLEnum,
    Index,
    TypeDecorator,
    BINARY,
    CHAR
)
from app.db.base import Base


class TodoStatus(str, enum.Enum):
    PENDING = "pending"
    PROGRESS = "progress"
    DONE = "done"


class TodoPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class UUIDv7Binary(TypeDecorator):
    """
    SQLAlchemy TypeDecorator storing UUID v7 as BINARY(16) in MySQL/relational databases
    and returning canonical 36-char UUID string to Python.
    """
    impl = BINARY(16)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "mysql":
            return dialect.type_descriptor(BINARY(16))
        return dialect.type_descriptor(BINARY(16))

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, bytes):
            return value
        if isinstance(value, str):
            return UUID(value).bytes
        if isinstance(value, UUID):
            return value.bytes
        raise ValueError(f"Invalid UUID value: {value}")

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, bytes):
            return str(UUID(bytes=value))
        return str(UUID(str(value)))


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Todo(Base):
    __tablename__ = "todos"

    id = Column(UUIDv7Binary, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(
        SQLEnum(TodoStatus, values_callable=lambda obj: [e.value for e in obj], native_enum=True),
        nullable=False,
        default=TodoStatus.PENDING
    )
    priority = Column(
        SQLEnum(TodoPriority, values_callable=lambda obj: [e.value for e in obj], native_enum=True),
        nullable=False,
        default=TodoPriority.MEDIUM
    )
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=False), nullable=False, default=utc_now)
    updated_at = Column(DateTime(timezone=False), nullable=False, default=utc_now, onupdate=utc_now)

    __table_args__ = (
        Index("idx_todos_status_created", "status", "created_at", "id"),
        Index("idx_todos_priority_created", "priority", "created_at", "id"),
    )
