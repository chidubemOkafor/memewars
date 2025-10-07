"""added created_at column for vote

Revision ID: 0abbd886047a
Revises: dea426e1a12d
Create Date: 2025-10-06 23:05:52.958347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0abbd886047a'
down_revision: Union[str, Sequence[str], None] = 'dea426e1a12d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
