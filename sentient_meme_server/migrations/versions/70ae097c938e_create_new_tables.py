"""create new tables

Revision ID: 70ae097c938e
Revises: 8c266bed1277
Create Date: 2025-10-04 18:30:37.902402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70ae097c938e'
down_revision: Union[str, Sequence[str], None] = '8c266bed1277'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
