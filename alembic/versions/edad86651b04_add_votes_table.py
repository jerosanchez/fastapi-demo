"""add votes table

Revision ID: edad86651b04
Revises: 486599c703d4
Create Date: 2025-10-16 17:21:13.568295

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "edad86651b04"
down_revision: Union[str, Sequence[str], None] = "486599c703d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "votes",
        sa.Column("post_id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("post_id", "user_id"),
        sa.ForeignKeyConstraint(
            ["post_id"], ["posts.id"], name="votes_post_id_fkey", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="votes_user_id_fkey", ondelete="CASCADE"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("votes")
