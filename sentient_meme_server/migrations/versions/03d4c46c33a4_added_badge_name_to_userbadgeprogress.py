"""added badge_name to UserBadgeProgress

Revision ID: 03d4c46c33a4
Revises: 0abbd886047a
Create Date: 2025-10-07 00:24:57.635878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03d4c46c33a4'
down_revision: Union[str, Sequence[str], None] = '0abbd886047a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
