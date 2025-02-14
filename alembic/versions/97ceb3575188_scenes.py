"""scenes

Revision ID: 97ceb3575188
Revises: 6e6beec245c1
Create Date: 2025-02-11 20:05:44.369496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97ceb3575188'
down_revision: Union[str, None] = '6e6beec245c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'scene',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type', sa.String)
    )
    op.create_table(
        'ending',
        sa.Column(
            'id',
            sa.Integer,
            sa.ForeignKey('scene.id'),
            primary_key=True,
        ),
        sa.Column('message', sa.String)
    )


def downgrade() -> None:
    op.drop_table('scene')
    op.drop_table('ending')
