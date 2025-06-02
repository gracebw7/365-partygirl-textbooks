"""delete duplicate table.

Revision ID: 50f7e0fc8b20
Revises: 934c5967ef74
Create Date: 2025-05-05 13:31:33.191095

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "50f7e0fc8b20"
down_revision: Union[str, None] = "934c5967ef74"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table("classbooks")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "classbooks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("class_id", sa.Integer, sa.ForeignKey("classes.id"), nullable=False),
        sa.Column(
            "textbook_id", sa.Integer, sa.ForeignKey("textbooks.id"), nullable=False
        ),
    )
