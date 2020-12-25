"""Add original_url column

Revision ID: 36b9a286cf28
Revises: c2d3c4a1a8d0
Create Date: 2020-12-25 01:41:03.082716

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "36b9a286cf28"
down_revision = "c2d3c4a1a8d0"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "link", sa.Column("original_url", sa.String(length=160), nullable=True)
    )


def downgrade():
    op.drop_column("link", "original_url")
