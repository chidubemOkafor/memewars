"""create badge userbadge meme tables 

Revision ID: b93af05e7852
Revises: 9a2d579c08cf
Create Date: 2025-10-04 18:26:18.428687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b93af05e7852'
down_revision: Union[str, Sequence[str], None] = '9a2d579c08cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
