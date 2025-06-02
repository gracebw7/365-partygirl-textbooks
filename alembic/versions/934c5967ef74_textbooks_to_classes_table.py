"""textbooks to classes table.

Revision ID: 934c5967ef74
Revises: 75b823e6bd44
Create Date: 2025-05-05 13:25:56.041227

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "934c5967ef74"
down_revision: Union[str, None] = "75b823e6bd44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "classbooks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("class_id", sa.Integer, sa.ForeignKey("classes.id"), nullable=False),
        sa.Column(
            "textbook_id", sa.Integer, sa.ForeignKey("textbooks.id"), nullable=False
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("classbooks")
