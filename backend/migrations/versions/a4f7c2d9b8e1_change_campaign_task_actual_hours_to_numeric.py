"""change campaign task actual_hours to numeric

Revision ID: a4f7c2d9b8e1
Revises: 5d7a9f0c1b22
Create Date: 2026-07-18 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a4f7c2d9b8e1"
down_revision: Union[str, Sequence[str], None] = "5d7a9f0c1b22"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "campaign_tasks",
        "actual_hours",
        existing_type=sa.Integer(),
        type_=sa.Numeric(8, 2),
        existing_nullable=True,
        postgresql_using="actual_hours::numeric(8, 2)",
    )


def downgrade() -> None:
    op.alter_column(
        "campaign_tasks",
        "actual_hours",
        existing_type=sa.Numeric(8, 2),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using="ROUND(actual_hours)::integer",
    )
