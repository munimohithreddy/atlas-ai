"""merge campaign foundation migration head

Revision ID: c3239c8715dd
Revises: 0a806526de3e, 9a8b7c6d5e4f
Create Date: 2026-07-17 20:03:10.554039

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3239c8715dd'
down_revision: Union[str, Sequence[str], None] = ('0a806526de3e', '9a8b7c6d5e4f')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
