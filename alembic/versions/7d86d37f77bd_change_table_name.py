"""change table name

Revision ID: 7d86d37f77bd
Revises: 50f7e0fc8b20
Create Date: 2025-05-05 16:54:49.176855

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7d86d37f77bd"
down_revision: Union[str, None] = "50f7e0fc8b20"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("textbook-classes", "textbook_classes")


def downgrade() -> None:
    """Downgrade schema."""
    pass
