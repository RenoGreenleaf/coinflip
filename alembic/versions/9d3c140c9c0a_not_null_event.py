"""not null event

Revision ID: 9d3c140c9c0a
Revises: ce4b8101d9fc
Create Date: 2025-03-07 20:35:21.228829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d3c140c9c0a'
down_revision: Union[str, None] = 'ce4b8101d9fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('event') as batch_op:
        batch_op.alter_column(
            'name',
            server_default=''
        )


def downgrade() -> None:
    pass
