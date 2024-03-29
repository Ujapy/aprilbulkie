"""added extra column in user table

Revision ID: 0c4eff58dfe9
Revises: ad8adc13d55f
Create Date: 2019-04-02 15:24:24.480904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c4eff58dfe9'
down_revision = 'ad8adc13d55f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('registered_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'registered_on')
    # ### end Alembic commands ###
