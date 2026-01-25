"""init

Revision ID: 5b0324d3e614
Revises: 9d0b6c15427c
Create Date: 2026-01-25 22:45:50.359836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b0324d3e614'
down_revision: Union[str, Sequence[str], None] = '9d0b6c15427c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
