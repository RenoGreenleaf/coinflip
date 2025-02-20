"""discoverable location

Revision ID: ecdf26a10396
Revises: fa5e99580338
Create Date: 2025-02-20 16:34:21.611474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecdf26a10396'
down_revision: Union[str, None] = 'fa5e99580338'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('location') as batch_op:
        batch_op.add_column(
            sa.Column(
                'discovered_event_id',
                sa.Integer,
                sa.ForeignKey('event.id', name='discovered_event')
            )
        )


def downgrade() -> None:
    with op.batch_alter_table('location') as batch_op:
        batch_op.drop_column('discovered_event_id')
