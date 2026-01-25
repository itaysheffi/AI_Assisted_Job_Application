"""init

Revision ID: 8d41f02e8615
Revises: 5b0324d3e614
Create Date: 2026-01-25 22:50:14.638730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d41f02e8615'
down_revision: Union[str, Sequence[str], None] = '5b0324d3e614'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
