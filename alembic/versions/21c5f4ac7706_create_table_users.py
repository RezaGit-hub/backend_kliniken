"""create table users

Revision ID: 21c5f4ac7706
Revises: 
Create Date: 2026-03-22 19:41:04.665256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21c5f4ac7706'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("email", sa.String(200), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.Text, nullable=False),
        sa.Column("role", sa.String(40), nullable=False, server_default="user"),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.func.now())
    )
    pass


def downgrade():
    op.drop_table("users")
    pass
