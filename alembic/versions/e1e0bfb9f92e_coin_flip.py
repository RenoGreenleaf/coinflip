"""coin flip

Revision ID: e1e0bfb9f92e
Revises: bf2750458b3f
Create Date: 2025-03-02 17:57:14.557406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1e0bfb9f92e'
down_revision: Union[str, None] = 'bf2750458b3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'coin_flip',
        sa.Column(
            'id',
            sa.Integer,
            sa.ForeignKey('scene.id'),
            primary_key=True,
        ),
        sa.Column('won_event_id', sa.Integer, sa.ForeignKey('event.id'))
    )


def downgrade() -> None:
    op.drop_table('coin_flip')
