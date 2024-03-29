"""added extra column in user table

Revision ID: ad8adc13d55f
Revises: 3c8a72f6f97c
Create Date: 2019-04-02 15:16:39.305161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad8adc13d55f'
down_revision = '3c8a72f6f97c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('current_logged_in', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'current_logged_in')
    # ### end Alembic commands ###
