"""starting scene

Revision ID: 5d6da1ac4fc8
Revises: 3ccd43f0cb06
Create Date: 2025-02-26 15:42:08.585914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d6da1ac4fc8'
down_revision: Union[str, None] = '3ccd43f0cb06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('state_machine') as batch_op:
        batch_op.add_column(
            sa.Column(
                'start_id',
                sa.Integer,
                sa.ForeignKey('scene.id', name='start_scene')
            )
        )


def downgrade() -> None:
    with op.batch_alter_table('state_machine') as batch_op:
        batch_op.drop_column('start_id')
