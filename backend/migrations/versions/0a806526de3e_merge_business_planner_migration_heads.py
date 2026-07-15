"""merge business planner migration heads

Revision ID: 0a806526de3e
Revises: 2b3c4d5e6f70, 8c7d6b5a4f21
Create Date: 2026-07-14 21:16:31.063645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a806526de3e'
down_revision: Union[str, Sequence[str], None] = ('2b3c4d5e6f70', '8c7d6b5a4f21')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
