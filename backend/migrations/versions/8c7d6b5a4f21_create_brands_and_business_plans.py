"""create brands and business plans

Revision ID: 8c7d6b5a4f21
Revises: 0f1a2b3c4d5e
Create Date: 2026-07-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "8c7d6b5a4f21"
down_revision: Union[str, Sequence[str], None] = "0f1a2b3c4d5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "brands",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("market", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug", name="uq_brands_slug"),
    )
    op.create_index(op.f("ix_brands_id"), "brands", ["id"], unique=False)
    op.create_index(op.f("ix_brands_name"), "brands", ["name"], unique=False)
    op.create_index(op.f("ix_brands_market"), "brands", ["market"], unique=False)
    op.create_index(op.f("ix_brands_slug"), "brands", ["slug"], unique=False)

    op.create_table(
        "business_plans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("brand_id", sa.Integer(), nullable=True),
        sa.Column("primary_monetization", sa.String(length=50), nullable=False),
        sa.Column("secondary_monetization", sa.String(length=50), nullable=True),
        sa.Column("primary_acquisition_channel", sa.String(length=50), nullable=False),
        sa.Column("secondary_acquisition_channels", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("recommended_assets", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("target_audience", sa.Text(), nullable=False),
        sa.Column("value_proposition", sa.Text(), nullable=False),
        sa.Column("revenue_low_monthly", sa.Integer(), nullable=False),
        sa.Column("revenue_high_monthly", sa.Integer(), nullable=False),
        sa.Column("revenue_confidence_score", sa.Integer(), nullable=False),
        sa.Column("effort_level", sa.String(length=20), nullable=False),
        sa.Column("estimated_launch_days", sa.Integer(), nullable=False),
        sa.Column("recommendation_summary", sa.Text(), nullable=False),
        sa.Column("next_action", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["brand_id"], ["brands.id"]),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("opportunity_id"),
    )
    op.create_index(op.f("ix_business_plans_id"), "business_plans", ["id"], unique=False)
    op.create_index(
        op.f("ix_business_plans_brand_id"),
        "business_plans",
        ["brand_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_business_plans_opportunity_id"),
        "business_plans",
        ["opportunity_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_business_plans_opportunity_id"), table_name="business_plans")
    op.drop_index(op.f("ix_business_plans_brand_id"), table_name="business_plans")
    op.drop_index(op.f("ix_business_plans_id"), table_name="business_plans")
    op.drop_table("business_plans")

    op.drop_index(op.f("ix_brands_slug"), table_name="brands")
    op.drop_index(op.f("ix_brands_market"), table_name="brands")
    op.drop_index(op.f("ix_brands_name"), table_name="brands")
    op.drop_index(op.f("ix_brands_id"), table_name="brands")
    op.drop_table("brands")
