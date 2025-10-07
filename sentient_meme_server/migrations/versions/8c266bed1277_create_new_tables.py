"""create new tables

Revision ID: 8c266bed1277
Revises: b93af05e7852
Create Date: 2025-10-04 18:28:19.093884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c266bed1277'
down_revision: Union[str, Sequence[str], None] = 'b93af05e7852'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
