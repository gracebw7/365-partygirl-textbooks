"""Add initial tables

Revision ID: 8e62621aad6e
Revises: f02d7ab62aac
Create Date: 2025-05-04 18:32:42.569513

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8e62621aad6e"
down_revision: Union[str, None] = "f02d7ab62aac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "courses",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("department", sa.Text, nullable=False),
        sa.Column("number", sa.Integer, nullable=False),
    )

    op.create_table(
        "professors",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first", sa.Text, nullable=False),
        sa.Column("last", sa.Text, nullable=False),
    )

    op.create_table(
        "classes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("course_id", sa.Integer, sa.ForeignKey("courses.id"), nullable=False),
        sa.Column(
            "professor_id", sa.Integer, sa.ForeignKey("professors.id"), nullable=False
        ),
    )

    op.create_table(
        "textbooks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("author", sa.Text, nullable=False),
        sa.Column("edition", sa.Text, nullable=True),
    )

    op.create_table(
        "links",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "creation_at", sa.TIMESTAMP, server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "textbook_id",
            sa.Integer,
            sa.ForeignKey("textbooks.id"),
            nullable=False,
        ),
        sa.Column("url", sa.Text, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("links")
    op.drop_table("classes")
    op.drop_table("textbooks")
    op.drop_table("courses")
    op.drop_table("professors")
