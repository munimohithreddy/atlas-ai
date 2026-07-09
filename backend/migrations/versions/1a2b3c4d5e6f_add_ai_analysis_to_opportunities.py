"""add ai analysis to opportunities

Revision ID: 1a2b3c4d5e6f
Revises: 0f1a2b3c4d5e
Create Date: 2026-07-09 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1a2b3c4d5e6f"
down_revision: Union[str, Sequence[str], None] = "0f1a2b3c4d5e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "opportunities",
        sa.Column("ai_executive_summary", sa.Text(), nullable=True),
    )
    op.add_column(
        "opportunities",
        sa.Column("ai_key_strengths", sa.JSON(), nullable=True),
    )
    op.add_column(
        "opportunities",
        sa.Column("ai_key_risks", sa.JSON(), nullable=True),
    )
    op.add_column(
        "opportunities",
        sa.Column("ai_recommendation_reason", sa.Text(), nullable=True),
    )
    op.add_column(
        "opportunities",
        sa.Column("ai_suggested_next_actions", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("opportunities", "ai_suggested_next_actions")
    op.drop_column("opportunities", "ai_recommendation_reason")
    op.drop_column("opportunities", "ai_key_risks")
    op.drop_column("opportunities", "ai_key_strengths")
    op.drop_column("opportunities", "ai_executive_summary")
