"""diaries_meal_products name changed to product_name

Revision ID: 0ac1def0a604
Revises: fb37144ee9e9
Create Date: 2026-07-24 19:45:19.958613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ac1def0a604'
down_revision: Union[str, Sequence[str], None] = 'fb37144ee9e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'diaries_meal_products',
        'name',
        new_column_name='product_name',
    )

def downgrade() -> None:
    op.alter_column(
        'diaries_meal_products',
        'product_name',
        new_column_name='name',
    )