"""exit event

Revision ID: bf2750458b3f
Revises: 5d6da1ac4fc8
Create Date: 2025-02-27 16:45:54.865859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf2750458b3f'
down_revision: Union[str, None] = '5d6da1ac4fc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('location_exit') as batch_op:
        batch_op.add_column(
            sa.Column(
                'triggers_event_id',
                sa.Integer,
                sa.ForeignKey('event.id', name='triggers_event')
            )
        )


def downgrade() -> None:
    with op.batch_alter_table('location_exit') as batch_op:
        batch_op.drop_column('triggers_event_id')
