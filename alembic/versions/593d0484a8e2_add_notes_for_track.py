"""Add notes for track

Revision ID: 593d0484a8e2
Revises: 9de71651198c
Create Date: 2024-05-08 23:55:44.358305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '593d0484a8e2'
down_revision: Union[str, None] = '9de71651198c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('track', sa.Column('notes', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('track', 'notes')
    # ### end Alembic commands ###
