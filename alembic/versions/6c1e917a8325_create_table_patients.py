"""create table patients

Revision ID: 6c1e917a8325
Revises: 21c5f4ac7706
Create Date: 2026-03-22 20:46:06.332574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c1e917a8325'
down_revision: Union[str, Sequence[str], None] = '21c5f4ac7706'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(40), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False),
        sa.Column("birth_date", sa.Date, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column("gender", sa.String(15), nullable=False),
        sa.Column("phone_nummer", sa.Integer, nullable=False)
    )
    pass


def downgrade():
    op.drop_table("patients")
    """Downgrade schema."""
    pass
