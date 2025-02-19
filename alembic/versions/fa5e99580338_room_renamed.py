"""room renamed

Revision ID: fa5e99580338
Revises: a2f29faf18b6
Create Date: 2025-02-19 20:51:48.539557

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'fa5e99580338'
down_revision: Union[str, None] = 'a2f29faf18b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('room', 'location')
    op.rename_table('room_exit', 'location_exit')
    op.alter_column('location_exit', 'room_id', new_column_name='location_id')


def downgrade() -> None:
    op.rename_table('location', 'room')
    op.rename_table('location_exit', 'room_exit')
    op.alter_column('room_exit', 'location_id', new_column_name='room_id')
