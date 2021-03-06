"""empty message

Revision ID: c538097f1991
Revises: 0c18ff62b414
Create Date: 2021-07-13 19:46:55.260295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c538097f1991'
down_revision = '0c18ff62b414'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'image_profile')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image_profile', sa.VARCHAR(length=20), nullable=True))
    # ### end Alembic commands ###
