"""Add email to professor table

Revision ID: 7688a271922d
Revises: bbb8daf90853
Create Date: 2025-05-23 13:32:14.104974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7688a271922d'
down_revision: Union[str, None] = 'bbb8daf90853'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("professors", sa.Column("email", sa.Text, unique=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
