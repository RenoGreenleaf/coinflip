"""exploration

Revision ID: a2f29faf18b6
Revises: 97ceb3575188
Create Date: 2025-02-16 13:46:57.728153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2f29faf18b6'
down_revision: Union[str, None] = '97ceb3575188'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'room',
        sa.Column(
            'id',
            sa.Integer,
            sa.ForeignKey('scene.id'),
            primary_key=True
        ),
        sa.Column('description', sa.String)
    )
    op.create_table(
        'room_exit',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('room_id', sa.Integer, sa.ForeignKey('room.id')),
        sa.Column('name', sa.String(255))
    )


def downgrade() -> None:
    op.drop_table('room_exit')
    op.drop_table('room')
