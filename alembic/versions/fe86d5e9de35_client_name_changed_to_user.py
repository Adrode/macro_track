"""client name changed to user

Revision ID: fe86d5e9de35
Revises: 8b572f06d7b3
Create Date: 2026-07-30 17:49:25.269226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'fe86d5e9de35'
down_revision: Union[str, Sequence[str], None] = '8b572f06d7b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table('trainer_client', 'trainer_user')
    op.alter_column('trainer_user', 'client_id', new_column_name='user_id')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('trainer_user', 'user_id', new_column_name='client_id')
    op.rename_table('trainer_user', 'trainer_client')
