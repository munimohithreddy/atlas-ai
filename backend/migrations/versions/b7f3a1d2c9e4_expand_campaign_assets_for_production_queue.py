"""expand campaign assets for production queue

Revision ID: b7f3a1d2c9e4
Revises: a4f7c2d9b8e1
Create Date: 2026-07-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7f3a1d2c9e4"
down_revision: Union[str, Sequence[str], None] = "a4f7c2d9b8e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("campaign_assets", sa.Column("campaign_task_id", sa.Integer(), nullable=True))
    op.add_column("campaign_assets", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("campaign_assets", sa.Column("priority", sa.String(length=20), nullable=False, server_default="medium"))
    op.add_column("campaign_assets", sa.Column("content_brief", sa.Text(), nullable=True))
    op.add_column("campaign_assets", sa.Column("target_audience", sa.Text(), nullable=True))
    op.add_column("campaign_assets", sa.Column("primary_keyword", sa.String(length=255), nullable=True))
    op.add_column("campaign_assets", sa.Column("secondary_keywords", sa.Text(), nullable=True))
    op.add_column("campaign_assets", sa.Column("call_to_action", sa.Text(), nullable=True))
    op.add_column("campaign_assets", sa.Column("assigned_to", sa.String(length=255), nullable=True))
    op.add_column("campaign_assets", sa.Column("estimated_hours", sa.Numeric(8, 2), nullable=True))
    op.add_column("campaign_assets", sa.Column("actual_hours", sa.Numeric(8, 2), nullable=True))
    op.add_column("campaign_assets", sa.Column("due_date", sa.DateTime(timezone=True), nullable=True))
    op.add_column("campaign_assets", sa.Column("started_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("campaign_assets", sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("campaign_assets", sa.Column("blocked_reason", sa.Text(), nullable=True))
    op.add_column("campaign_assets", sa.Column("review_notes", sa.Text(), nullable=True))
    op.add_column("campaign_assets", sa.Column("rejection_reason", sa.Text(), nullable=True))
    op.add_column("campaign_assets", sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("campaign_assets", sa.Column("order_index", sa.Integer(), nullable=True))
    op.execute("UPDATE campaign_assets SET order_index = id WHERE order_index IS NULL")
    op.alter_column("campaign_assets", "order_index", nullable=False)
    op.create_index(op.f("ix_campaign_assets_priority"), "campaign_assets", ["priority"], unique=False)
    op.create_index(op.f("ix_campaign_assets_order_index"), "campaign_assets", ["order_index"], unique=False)
    op.create_index(op.f("ix_campaign_assets_campaign_task_id"), "campaign_assets", ["campaign_task_id"], unique=False)
    op.create_foreign_key(
        "fk_campaign_assets_campaign_task_id_campaign_tasks",
        "campaign_assets",
        "campaign_tasks",
        ["campaign_task_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_campaign_assets_campaign_task_id_campaign_tasks", "campaign_assets", type_="foreignkey")
    op.drop_index(op.f("ix_campaign_assets_campaign_task_id"), table_name="campaign_assets")
    op.drop_index(op.f("ix_campaign_assets_order_index"), table_name="campaign_assets")
    op.drop_index(op.f("ix_campaign_assets_priority"), table_name="campaign_assets")
    op.drop_column("campaign_assets", "order_index")
    op.drop_column("campaign_assets", "approved_at")
    op.drop_column("campaign_assets", "rejection_reason")
    op.drop_column("campaign_assets", "review_notes")
    op.drop_column("campaign_assets", "blocked_reason")
    op.drop_column("campaign_assets", "completed_at")
    op.drop_column("campaign_assets", "started_at")
    op.drop_column("campaign_assets", "due_date")
    op.drop_column("campaign_assets", "actual_hours")
    op.drop_column("campaign_assets", "estimated_hours")
    op.drop_column("campaign_assets", "assigned_to")
    op.drop_column("campaign_assets", "call_to_action")
    op.drop_column("campaign_assets", "secondary_keywords")
    op.drop_column("campaign_assets", "primary_keyword")
    op.drop_column("campaign_assets", "target_audience")
    op.drop_column("campaign_assets", "content_brief")
    op.drop_column("campaign_assets", "priority")
    op.drop_column("campaign_assets", "description")
    op.drop_column("campaign_assets", "campaign_task_id")
