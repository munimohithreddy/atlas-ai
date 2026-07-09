"""create opportunity evidence table

Revision ID: 0f1a2b3c4d5e
Revises: 7149e72db894
Create Date: 2026-07-09 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0f1a2b3c4d5e"
down_revision: Union[str, Sequence[str], None] = "7149e72db894"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "opportunity_evidence",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(length=100), nullable=False),
        sa.Column("signal_type", sa.String(length=100), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("confidence_score", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_opportunity_evidence_id"),
        "opportunity_evidence",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_opportunity_evidence_opportunity_id"),
        "opportunity_evidence",
        ["opportunity_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_opportunity_evidence_signal_type"),
        "opportunity_evidence",
        ["signal_type"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_opportunity_evidence_signal_type"),
        table_name="opportunity_evidence",
    )
    op.drop_index(
        op.f("ix_opportunity_evidence_opportunity_id"),
        table_name="opportunity_evidence",
    )
    op.drop_index(op.f("ix_opportunity_evidence_id"), table_name="opportunity_evidence")
    op.drop_table("opportunity_evidence")
