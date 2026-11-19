"""001_create_todos_table

Revision ID: 001_initial
Revises: 
Create Date: 2026-11-19 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    is_mysql = bind.dialect.name == "mysql"

    if is_mysql:
        status_enum = mysql.ENUM('pending', 'progress', 'done')
        priority_enum = mysql.ENUM('low', 'medium', 'high')
    else:
        status_enum = sa.Enum('pending', 'progress', 'done', name='todostatus')
        priority_enum = sa.Enum('low', 'medium', 'high', name='todopriority')

    op.create_table(
        'todos',
        sa.Column('id', sa.BINARY(16), primary_key=True, nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('status', status_enum, nullable=False, server_default='pending'),
        sa.Column('priority', priority_enum, nullable=False, server_default='medium'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=False), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_index('idx_todos_status_created', 'todos', ['status', 'created_at', 'id'])
    op.create_index('idx_todos_priority_created', 'todos', ['priority', 'created_at', 'id'])


def downgrade() -> None:
    op.drop_index('idx_todos_priority_created', table_name='todos')
    op.drop_index('idx_todos_status_created', table_name='todos')
    op.drop_table('todos')
