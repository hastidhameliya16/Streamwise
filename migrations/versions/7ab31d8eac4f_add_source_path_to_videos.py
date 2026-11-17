"""add source path to videos

Revision ID: 7ab31d8eac4f
Revises: c11b643c836b
Create Date: 2026-11-17

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7ab31d8eac4f"
down_revision: Union[str, Sequence[str], None] = "c11b643c836b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("videos", sa.Column("source_path", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("videos", "source_path")
