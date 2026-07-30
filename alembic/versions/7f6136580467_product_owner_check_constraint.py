"""product owner check constraint

Revision ID: 7f6136580467
Revises: fe86d5e9de35
Create Date: 2026-07-30 18:53:57.315145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f6136580467'
down_revision: Union[str, Sequence[str], None] = 'fe86d5e9de35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint(
        constraint_name="product_owner_check",
        table_name="products",
        condition="((user_id IS NULL) AND (trainer_id IS NOT NULL)) OR ((user_id IS NOT NULL) AND (trainer_id IS NULL)) OR ((user_id IS NULL) AND (trainer_id IS NULL))",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("product_owner_check", "products", type_="check")
