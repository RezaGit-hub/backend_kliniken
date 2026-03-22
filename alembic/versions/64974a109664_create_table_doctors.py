"""create table doctors

Revision ID: 64974a109664
Revises: 6c1e917a8325
Create Date: 2026-03-22 21:04:05.503232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64974a109664'
down_revision: Union[str, Sequence[str], None] = '6c1e917a8325'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "doctors",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False),
        sa.Column("specialization", sa.String(20), nullable=False),
        sa.Column("phone_nummer", sa.Integer, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=sa.func.now())
    )
    pass


def downgrade() :
    op.drop_table("doctors")
    pass
