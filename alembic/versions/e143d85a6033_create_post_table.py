"""Create Post Table

Revision ID: e143d85a6033
Revises: 
Create Date: 2026-02-22 23:43:58.455362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e143d85a6033'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('post',
                    sa.Column('id', sa.Integer(), nullable=False,),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), nullable=False, server_default='True'),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    primary_key=['id']
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('post')
