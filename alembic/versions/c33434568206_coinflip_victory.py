"""coinflip victory

Revision ID: c33434568206
Revises: e1e0bfb9f92e
Create Date: 2025-03-04 16:17:12.559680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c33434568206'
down_revision: Union[str, None] = 'e1e0bfb9f92e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('coin_flip', sa.Column('victory_threshold', sa.Integer))


def downgrade() -> None:
    op.drop_column('coin_flip', 'victory_threshold')
