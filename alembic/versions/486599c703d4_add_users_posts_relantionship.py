"""add users-posts relantionship

Revision ID: 486599c703d4
Revises: 940914ec11f1
Create Date: 2025-10-16 17:13:21.424147

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "486599c703d4"
down_revision: Union[str, Sequence[str], None] = "940914ec11f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add owner_id column to posts table
    op.add_column("posts", sa.Column("owner_id", sa.String(), nullable=False))

    # Create foreign key constraint
    op.create_foreign_key(
        "posts_owner_id_fkey",
        "posts",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign key constraint
    op.drop_constraint("posts_owner_id_fkey", "posts", type_="foreignkey")

    # Drop owner_id column
    op.drop_column("posts", "owner_id")
