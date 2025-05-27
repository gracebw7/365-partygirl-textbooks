"""add uniqueness constraints

Revision ID: 682daa378756
Revises: 7688a271922d
Create Date: 2025-05-26 18:54:59.891073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '682daa378756'
down_revision: Union[str, None] = '7688a271922d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add uniqueness constraints to the professors table
    op.create_unique_constraint(
        'uq_professors_email',
        'professors',
        ['email']
    )
    # Add uniqueness constraint to delete_link_requests to combo of link_id and description
    op.create_unique_constraint(
        'uq_delete_link_requests_link_id_description',
        'delete_link_requests',
        ['link_id', 'description']
    )
    # Add uniqueness constraing to courses (combo of department and number)
    op.create_unique_constraint(
        'uq_courses_department_number',
        'courses',
        ['department', 'number']
    )
    # add uniqueness constraing to classes for combo of course_id and professor_id
    op.create_unique_constraint(
        'uq_classes_course_id_professor_id',
        'classes',
        ['course_id', 'professor_id']
    )
    # Add uniqueness constraint to textbooks for title, author, and edition
    op.create_unique_constraint(
        'uq_textbooks_title_author_edition',
        'textbooks',
        ['title', 'author', 'edition']
    )
    # Add uniqueness constraint to textbook_classes for textbook_id and class_id
    op.create_unique_constraint(
        'uq_textbook_classes_textbook_id_class_id',
        'textbook_classes',
        ['textbook_id', 'class_id']
    )
    # add uniqueness constraing to links for tetbook_id and url combo
    op.create_unique_constraint(
        'uq_links_textbook_id_url',
        'links',
        ['textbook_id', 'url']
    )

    pass


def downgrade() -> None:
    """Downgrade schema."""
    # Remove uniqueness constraints from the professors table
    op.drop_constraint(
        'uq_professors_email',
        'professors',
        type_='unique'
    )
    # Remove uniqueness constraint from delete_link_requests to combo of link_id and description
    op.drop_constraint(
        'uq_delete_link_requests_link_id_description',
        'delete_link_requests',
        type_='unique'
    )
    # Remove uniqueness constraing from courses (combo of department and number)
    op.drop_constraint(
        'uq_courses_department_number',
        'courses',
        type_='unique'
    )
    # remove uniqueness constraing from classes for combo of course_id and professor_id
    op.drop_constraint(
        'uq_classes_course_id_professor_id',
        'classes',
        type_='unique'
    )
    # Remove uniqueness constraint from textbooks for title, author, and edition
    op.drop_constraint(
        'uq_textbooks_title_author_edition',
        'textbooks',
        type_='unique'
    )
    # Remove uniqueness constraint from textbook_classes for textbook_id and class_id
    op.drop_constraint(
        'uq_textbook_classes_textbook_id_class_id',
        'textbook_classes',
        type_='unique'
    )
    # remove uniqueness constraing from links for tetbook_id and url combo
    op.drop_constraint(
        'uq_links_textbook_id_url',
        'links',
        type_='unique'
    )
    pass
