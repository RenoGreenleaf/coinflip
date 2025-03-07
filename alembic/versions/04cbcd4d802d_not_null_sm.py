"""not null SM

Revision ID: 04cbcd4d802d
Revises: 446af636fd0a
Create Date: 2025-03-07 20:55:09.427553

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '04cbcd4d802d'
down_revision: Union[str, None] = '446af636fd0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('state_machine') as batch_op:
        batch_op.alter_column(
            'start_id',
            nullable=False,
        )

    with op.batch_alter_table('transition') as batch_op:
        batch_op.alter_column(
            'event_id',
            nullable=False,
        )
        batch_op.alter_column(
            'scene_id',
            nullable=False,
        )
        batch_op.alter_column(
            'state_machine_id',
            nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table('state_machine') as batch_op:
        batch_op.alter_column(
            'start_id',
            nullable=True,
        )

    with op.batch_alter_table('transition') as batch_op:
        batch_op.alter_column(
            'event_id',
            nullable=True,
        )
        batch_op.alter_column(
            'scene_id',
            nullable=True,
        )
        batch_op.alter_column(
            'state_machine_id',
            nullable=True,
        )
