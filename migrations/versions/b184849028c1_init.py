"""Init

Revision ID: b184849028c1
Revises: 
Create Date: 2023-11-05 18:08:31.621444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b184849028c1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('grades', 'grade',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('grades', 'grade_date',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('grades', 'grade_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('grades', 'grade',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###