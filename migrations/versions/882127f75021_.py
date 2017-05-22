"""empty message

Revision ID: 882127f75021
Revises: b9224fd3fa9d
Create Date: 2017-05-08 14:21:52.373671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '882127f75021'
down_revision = 'b9224fd3fa9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(length=50), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('bucketlist',
    sa.Column('bucket_id', sa.Integer(), nullable=False),
    sa.Column('bucket_name', sa.String(length=50), nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('bucket_id')
    )
    op.create_table('bucket_items',
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=50), nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('bucket_list_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bucket_list_id'], ['bucketlist.bucket_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bucket_items')
    op.drop_table('bucketlist')
    op.drop_table('users')
    # ### end Alembic commands ###