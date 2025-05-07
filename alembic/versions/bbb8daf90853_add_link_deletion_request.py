"""add link deletion request.

Revision ID: bbb8daf90853
Revises: 7d86d37f77bd
Create Date: 2025-05-07 13:32:11.899983

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbb8daf90853'
down_revision: Union[str, None] = '7d86d37f77bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "delete_link_requests",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("link_id", sa.Integer, sa.ForeignKey("links.id", ondelete="CASCADE"), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("delete_link_requests")
