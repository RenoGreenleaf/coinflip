"""lock

Revision ID: 90394552f72c
Revises: 58d1893c9aa2
Create Date: 2025-03-10 20:55:09.266225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90394552f72c'
down_revision: Union[str, None] = '58d1893c9aa2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'lock',
        sa.Column('id', sa.Integer, sa.ForeignKey('scene.id'), primary_key=True)
    )
    op.create_table(
        'lock_pin',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('is_clockwise', sa.Boolean, nullable=False),
        sa.Column('lock_id', sa.Integer, sa.ForeignKey('lock.id')),
        sa.Column('offset', sa.Integer, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('lock_pin')
    op.drop_table('lock')
