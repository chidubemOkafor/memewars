"""added relationships to userBadgeProgress table

Revision ID: dea426e1a12d
Revises: 9a59226e2b1c
Create Date: 2025-10-05 22:00:27.547492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dea426e1a12d'
down_revision: Union[str, Sequence[str], None] = '9a59226e2b1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
