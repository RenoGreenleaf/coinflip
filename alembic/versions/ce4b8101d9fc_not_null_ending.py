"""not null ending

Revision ID: ce4b8101d9fc
Revises: 95ecbb597050
Create Date: 2025-03-07 20:26:49.270935

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'ce4b8101d9fc'
down_revision: Union[str, None] = '95ecbb597050'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('ending') as batch_op:
        batch_op.alter_column(
            'message',
            nullable=False,
            server_default=''
        )

def downgrade() -> None:
    with op.batch_alter_table('ending') as batch_op:
        batch_op.alter_column(
            'message',
            nullable=True
        )
