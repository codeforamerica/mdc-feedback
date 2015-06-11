"""empty message

Revision ID: 51d482bf4ea1
Revises: 380fcc2279cc
Create Date: 2015-06-11 11:43:59.498189

"""

# revision identifiers, used by Alembic.
revision = '51d482bf4ea1'
down_revision = '380fcc2279cc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('surveys', sa.Column('quiz_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('surveys', 'quiz_id')
    ### end Alembic commands ###
