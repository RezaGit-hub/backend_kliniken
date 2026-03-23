"""create table appointments

Revision ID: e7abb587a559
Revises: 64974a109664
Create Date: 2026-03-23 19:11:09.712475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7abb587a559'
down_revision: Union[str, Sequence[str], None] = '64974a109664'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patient_id", sa.Integer, sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("doctor_id", sa.Integer, sa.ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("appointment_date", sa.DateTime, nullable=False),
        sa.Column("reason", sa.TEXT()),
        sa.Column("created_at", sa.TIMESTAMP, nullable=False, server_default=sa.func.now())
    )
    op.create_index("idx_patient_id", "appointments", ["patient_id"])
    op.create_index("idx_doctor_id", "appointments", ["doctor_id"])
    pass


def downgrade():
    op.drop_index("idx_patient_id", table_name="appointments")
    op.drop_index("idx_doctor_id", table_name="appointments")
    op.drop_table("appointments")
    pass
