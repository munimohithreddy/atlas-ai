"""create affiliate programs table

Revision ID: 2b3c4d5e6f70
Revises: 1a2b3c4d5e6f
Create Date: 2026-07-09 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2b3c4d5e6f70"
down_revision: Union[str, Sequence[str], None] = "1a2b3c4d5e6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "affiliate_programs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("network", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=255), nullable=False),
        sa.Column("website_url", sa.String(length=500), nullable=False),
        sa.Column("commission_type", sa.String(length=100), nullable=False),
        sa.Column("commission_rate", sa.Float(), nullable=False),
        sa.Column("cookie_duration_days", sa.Integer(), nullable=False),
        sa.Column("approval_required", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_affiliate_programs_category"),
        "affiliate_programs",
        ["category"],
        unique=False,
    )
    op.create_index(
        op.f("ix_affiliate_programs_id"),
        "affiliate_programs",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_affiliate_programs_name"),
        "affiliate_programs",
        ["name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_affiliate_programs_network"),
        "affiliate_programs",
        ["network"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_affiliate_programs_network"), table_name="affiliate_programs")
    op.drop_index(op.f("ix_affiliate_programs_name"), table_name="affiliate_programs")
    op.drop_index(op.f("ix_affiliate_programs_id"), table_name="affiliate_programs")
    op.drop_index(op.f("ix_affiliate_programs_category"), table_name="affiliate_programs")
    op.drop_table("affiliate_programs")
