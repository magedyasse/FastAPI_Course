"""add FK to post table

Revision ID: 6b0bbff27a66
Revises: 279bdf2c0b42
Create Date: 2026-02-23 00:25:58.809673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b0bbff27a66'
down_revision: Union[str, Sequence[str], None] = '279bdf2c0b42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('post', sa.Column('owner_id', sa.Integer(), nullable=False)) 
    op.create_foreign_key(
        'post_users_fk', 
        source_table='post', 
        referent_table='users', 
        local_cols=['owner_id'], 
        remote_cols=['id'], 
        ondelete='CASCADE'
        )
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_constraint('post_users_fk', 'posts', type_='foreignkey')
    
    op.drop_column('posts', 'owner_id') 

    pass
