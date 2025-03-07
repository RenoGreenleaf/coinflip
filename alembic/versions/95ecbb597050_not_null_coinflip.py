"""not null coinflip

Revision ID: 95ecbb597050
Revises: c33434568206
Create Date: 2025-03-07 19:06:18.823270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95ecbb597050'
down_revision: Union[str, None] = 'c33434568206'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('coin_flip') as batch_op:
        batch_op.alter_column(
            'victory_threshold',
            nullable=False,
            server_default='3'
        )
        batch_op.alter_column(
            'won_event_id',
            nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table('coin_flip') as batch_op:
        batch_op.alter_column(
            'victory_threshold',
            nullable=True,
            default=None
        )
        batch_op.alter_column(
            'won_event_id',
            nullable=True,
        )