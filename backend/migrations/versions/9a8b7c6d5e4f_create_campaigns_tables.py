"""create campaigns tables

Revision ID: 9a8b7c6d5e4f
Revises: 8c7d6b5a4f21
Create Date: 2026-07-18 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9a8b7c6d5e4f"
down_revision: Union[str, Sequence[str], None] = "8c7d6b5a4f21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "campaigns",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("business_plan_id", sa.Integer(), nullable=False),
        sa.Column("brand_id", sa.Integer(), nullable=True),
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("goal", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False),
        sa.Column("expected_monthly_revenue", sa.Integer(), nullable=False),
        sa.Column("estimated_build_hours", sa.Integer(), nullable=False),
        sa.Column("launch_target_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["business_plan_id"], ["business_plans.id"]),
        sa.ForeignKeyConstraint(["brand_id"], ["brands.id"]),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("business_plan_id"),
        sa.UniqueConstraint("slug", name="uq_campaigns_slug"),
    )
    op.create_index(op.f("ix_campaigns_id"), "campaigns", ["id"], unique=False)
    op.create_index(op.f("ix_campaigns_business_plan_id"), "campaigns", ["business_plan_id"], unique=False)
    op.create_index(op.f("ix_campaigns_brand_id"), "campaigns", ["brand_id"], unique=False)
    op.create_index(op.f("ix_campaigns_opportunity_id"), "campaigns", ["opportunity_id"], unique=False)
    op.create_index(op.f("ix_campaigns_name"), "campaigns", ["name"], unique=False)
    op.create_index(op.f("ix_campaigns_slug"), "campaigns", ["slug"], unique=False)
    op.create_index(op.f("ix_campaigns_status"), "campaigns", ["status"], unique=False)
    op.create_index(op.f("ix_campaigns_priority"), "campaigns", ["priority"], unique=False)

    op.create_table(
        "campaign_tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("campaign_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False),
        sa.Column("estimated_hours", sa.Integer(), nullable=False),
        sa.Column("depends_on_task_id", sa.Integer(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaigns.id"]),
        sa.ForeignKeyConstraint(["depends_on_task_id"], ["campaign_tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_campaign_tasks_id"), "campaign_tasks", ["id"], unique=False)
    op.create_index(op.f("ix_campaign_tasks_campaign_id"), "campaign_tasks", ["campaign_id"], unique=False)
    op.create_index(op.f("ix_campaign_tasks_category"), "campaign_tasks", ["category"], unique=False)
    op.create_index(op.f("ix_campaign_tasks_depends_on_task_id"), "campaign_tasks", ["depends_on_task_id"], unique=False)
    op.create_index(op.f("ix_campaign_tasks_order_index"), "campaign_tasks", ["order_index"], unique=False)

    op.create_table(
        "campaign_assets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("campaign_id", sa.Integer(), nullable=False),
        sa.Column("asset_type", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("channel", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("planned_quantity", sa.Integer(), nullable=False),
        sa.Column("generated_quantity", sa.Integer(), nullable=False),
        sa.Column("published_quantity", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["campaign_id"], ["campaigns.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_campaign_assets_id"), "campaign_assets", ["id"], unique=False)
    op.create_index(op.f("ix_campaign_assets_campaign_id"), "campaign_assets", ["campaign_id"], unique=False)
    op.create_index(op.f("ix_campaign_assets_asset_type"), "campaign_assets", ["asset_type"], unique=False)
    op.create_index(op.f("ix_campaign_assets_channel"), "campaign_assets", ["channel"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_campaign_assets_channel"), table_name="campaign_assets")
    op.drop_index(op.f("ix_campaign_assets_asset_type"), table_name="campaign_assets")
    op.drop_index(op.f("ix_campaign_assets_campaign_id"), table_name="campaign_assets")
    op.drop_index(op.f("ix_campaign_assets_id"), table_name="campaign_assets")
    op.drop_table("campaign_assets")

    op.drop_index(op.f("ix_campaign_tasks_order_index"), table_name="campaign_tasks")
    op.drop_index(op.f("ix_campaign_tasks_depends_on_task_id"), table_name="campaign_tasks")
    op.drop_index(op.f("ix_campaign_tasks_category"), table_name="campaign_tasks")
    op.drop_index(op.f("ix_campaign_tasks_campaign_id"), table_name="campaign_tasks")
    op.drop_index(op.f("ix_campaign_tasks_id"), table_name="campaign_tasks")
    op.drop_table("campaign_tasks")

    op.drop_index(op.f("ix_campaigns_priority"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_status"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_slug"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_name"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_opportunity_id"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_brand_id"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_business_plan_id"), table_name="campaigns")
    op.drop_index(op.f("ix_campaigns_id"), table_name="campaigns")
    op.drop_table("campaigns")
