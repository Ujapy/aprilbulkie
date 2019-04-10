"""empty message

Revision ID: 39b762fa91ca
Revises: 
Create Date: 2019-03-25 23:28:43.973146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39b762fa91ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('firstname', sa.String(length=20), nullable=False),
    sa.Column('surname', sa.String(length=20), nullable=False),
    sa.Column('sex', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('address', sa.String(length=300), nullable=False),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.Column('phone2', sa.Integer(), nullable=True),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('phone2'),
    sa.UniqueConstraint('username')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_file', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=False),
    sa.Column('total_slot', sa.Integer(), nullable=False),
    sa.Column('slot_value', sa.Integer(), nullable=False),
    sa.Column('available_slot', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('location', sa.String(length=500), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('user')
    # ### end Alembic commands ###