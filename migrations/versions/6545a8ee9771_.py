"""empty message

Revision ID: 6545a8ee9771
Revises: 2c26a9639d45
Create Date: 2021-07-02 20:39:22.571620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6545a8ee9771'
down_revision = '2c26a9639d45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_seen', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('member_since', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'member_since')
    op.drop_column('users', 'last_seen')
    # ### end Alembic commands ###
