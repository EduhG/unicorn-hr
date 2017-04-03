"""empty message

Revision ID: 0ba710f51211
Revises: 298e76b3cb1c
Create Date: 2017-04-03 00:11:45.497109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ba710f51211'
down_revision = '298e76b3cb1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('full_name', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'full_name')
    # ### end Alembic commands ###
