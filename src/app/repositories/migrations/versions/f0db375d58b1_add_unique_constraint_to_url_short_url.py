"""add unique constraint to url.short_url

Revision ID: f0db375d58b1
Revises: 16b8e0c847c2
Create Date: 2024-07-25 10:39:48.077426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0db375d58b1'
down_revision: Union[str, None] = '16b8e0c847c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'urls', ['short_url'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'urls', type_='unique')
    # ### end Alembic commands ###
