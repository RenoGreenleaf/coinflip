"""state machine

Revision ID: 3ccd43f0cb06
Revises: 0748a394eca5
Create Date: 2025-02-24 19:17:17.229902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ccd43f0cb06'
down_revision: Union[str, None] = '0748a394eca5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'state_machine',
        sa.Column('id', sa.Integer, primary_key=True)
    )
    op.create_table(
        'transition',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('event_id', sa.Integer, sa.ForeignKey('event.id')),
        sa.Column('scene_id', sa.Integer, sa.ForeignKey('scene.id')),
        sa.Column('state_machine_id', sa.Integer, sa.ForeignKey('state_machine.id'))
    )


def downgrade() -> None:
    op.drop_table('transition')
    op.drop_table('state_machine')
