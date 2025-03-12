"""unlocked event

Revision ID: 5826dc9d0c3a
Revises: 90394552f72c
Create Date: 2025-03-12 17:29:31.639353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5826dc9d0c3a'
down_revision: Union[str, None] = '90394552f72c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('lock') as batch_op:
        batch_op.add_column(
            sa.Column(
                'unlocked_event_id',
                sa.Integer,
                sa.ForeignKey('event.id', name='unlocked_event'),
                nullable=False,
                default=0
            )
        )


def downgrade() -> None:
    with op.batch_alter_table('lock') as batch_op:
        batch_op.drop_column('unlocked_event_id')
