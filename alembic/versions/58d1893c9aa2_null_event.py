"""null event

Revision ID: 58d1893c9aa2
Revises: 04cbcd4d802d
Create Date: 2025-03-09 15:40:50.876027

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '58d1893c9aa2'
down_revision: Union[str, None] = '04cbcd4d802d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('coin_flip') as batch_op:
        batch_op.alter_column(
            'won_event_id',
            server_default='0'
        )

    with op.batch_alter_table('location') as batch_op:
        batch_op.alter_column(
            'discovered_event_id',
            server_default='0'
        )

    with op.batch_alter_table('location_exit') as batch_op:
        batch_op.alter_column(
            'location_id',
            server_default='0'
        )
        batch_op.alter_column(
            'triggers_event_id',
            server_default='0'
        )

    with op.batch_alter_table('state_machine') as batch_op:
        batch_op.alter_column(
            'start_id',
            server_default='0'
        )
