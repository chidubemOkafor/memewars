"""added userBadgeProgress table

Revision ID: 9a59226e2b1c
Revises: 11bef3d5f8df
Create Date: 2025-10-05 21:19:53.823530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a59226e2b1c'
down_revision: Union[str, Sequence[str], None] = '11bef3d5f8df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
