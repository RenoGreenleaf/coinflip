"""not null location

Revision ID: 446af636fd0a
Revises: 9d3c140c9c0a
Create Date: 2025-03-07 20:40:29.803556

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '446af636fd0a'
down_revision: Union[str, None] = '9d3c140c9c0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('location') as batch_op:
        batch_op.alter_column(
            'description',
            nullable=False,
            server_default=''
        )
        batch_op.alter_column(
            'discovered_event_id',
            nullable=False,
        )

    with op.batch_alter_table('location_exit') as batch_op:
        batch_op.alter_column(
            'location_id',
            nullable=False,
        )
        batch_op.alter_column(
            'name',
            nullable=False,
            server_default=''
        )
        batch_op.alter_column(
            'description',
            nullable=False,
            server_default=''
        )
        batch_op.alter_column(
            'triggers_event_id',
            nullable=False,
        )



def downgrade() -> None:
    with op.batch_alter_table('location') as batch_op:
        batch_op.alter_column(
            'description',
            nullable=True,
        )
        batch_op.alter_column(
            'discovered_event_id',
            nullable=True,
        )

    with op.batch_alter_table('location_exit') as batch_op:
        batch_op.alter_column(
            'location_id',
            nullable=True,
        )
        batch_op.alter_column(
            'name',
            nullable=True,
        )
        batch_op.alter_column(
            'description',
            nullable=True,
        )
        batch_op.alter_column(
            'triggers_event_id',
            nullable=True,
        )
