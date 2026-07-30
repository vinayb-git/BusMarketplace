"""add bus fleet number constraint

Revision ID: dc9554498aa4
Revises: 9339390c8d4e
Create Date: 2026-07-25 16:35:38.264215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc9554498aa4'
down_revision: Union[str, Sequence[str], None] = '9339390c8d4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_unique_constraint(
        "uq_bus_operator_fleet_number",
        "buses",
        ["operator_id", "fleet_number"],
    )


def downgrade():
    op.drop_constraint(
        "uq_bus_operator_fleet_number",
        "buses",
        type_="unique",
    )
