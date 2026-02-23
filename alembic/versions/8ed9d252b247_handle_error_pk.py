"""Handle error PK

Revision ID: 8ed9d252b247
Revises: e143d85a6033
Create Date: 2026-02-22 23:55:03.666112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ed9d252b247'
down_revision: Union[str, Sequence[str], None] = 'e143d85a6033'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'post',
        'id',
        existing_type=sa.Integer(),
        nullable=False
    )
    op.create_primary_key(
        'pk_post_id', 
        'post',
        ['id']
    )
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        'pk_post_id',
        'post',
        type_='primary'
    )
    
    pass
