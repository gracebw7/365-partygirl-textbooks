"""Added textbook-classes

Revision ID: 75b823e6bd44
Revises: 8e62621aad6e
Create Date: 2025-05-04 19:26:34.000734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75b823e6bd44'
down_revision: Union[str, None] = '8e62621aad6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "textbook-classes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("textbook_id", sa.Integer, sa.ForeignKey("textbooks.id"),
            nullable=False,),
        sa.Column("class_id", sa.Integer, sa.ForeignKey("classes.id"),
            nullable=False,)
    )


def downgrade() -> None:
    op.drop_table("textbook-classes")
