"""add campaign task execution fields

Revision ID: 5d7a9f0c1b22
Revises: c3239c8715dd
Create Date: 2026-07-18 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5d7a9f0c1b22"
down_revision: Union[str, Sequence[str], None] = "c3239c8715dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("campaign_tasks", sa.Column("started_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("campaign_tasks", sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("campaign_tasks", sa.Column("blocked_reason", sa.Text(), nullable=True))
    op.add_column("campaign_tasks", sa.Column("completion_notes", sa.Text(), nullable=True))
    op.add_column("campaign_tasks", sa.Column("actual_hours", sa.Integer(), nullable=True))
    op.add_column("campaign_tasks", sa.Column("assigned_to", sa.String(length=255), nullable=True))
    op.add_column("campaign_tasks", sa.Column("due_date", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("campaign_tasks", "due_date")
    op.drop_column("campaign_tasks", "assigned_to")
    op.drop_column("campaign_tasks", "actual_hours")
    op.drop_column("campaign_tasks", "completion_notes")
    op.drop_column("campaign_tasks", "blocked_reason")
    op.drop_column("campaign_tasks", "completed_at")
    op.drop_column("campaign_tasks", "started_at")
