"""conversation model

Revision ID: 1dbaa148f3a8
Revises: 5826dc9d0c3a
Create Date: 2025-03-13 19:34:52.588958

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1dbaa148f3a8'
down_revision: Union[str, None] = '5826dc9d0c3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'conversation',
        sa.Column(
            'id',
            sa.Integer,
            sa.ForeignKey('scene.id'),
            primary_key=True
        )
    )
    op.create_table(
        'conversation_option',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'conversation_id',
            sa.Integer,
            sa.ForeignKey('conversation.id'),
            nullable=False,
            default=0
        ),
        sa.Column('description', sa.String, nullable=False, default=""),
        sa.Column(
            'triggers_id',
            sa.Integer,
            sa.ForeignKey('event.id'),
            nullable=False,
            default=0
        ),
        sa.Column(
            'hide_id',
            sa.Integer,
            sa.ForeignKey('event.id'),
            nullable=False,
            default=0
        ),
        sa.Column(
            'show_id',
            sa.Integer,
            sa.ForeignKey('event.id'),
            nullable=False,
            default=0
        ),
        sa.Column('available', sa.Boolean, nullable=False, default=True),
        sa.Column('message', sa.String, nullable=False, default="")
    )


def downgrade() -> None:
    op.drop_table('conversation_option')
    op.drop_table('conversation')
