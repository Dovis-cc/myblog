"""empty message

Revision ID: b245668c166a
Revises: b01de4fa3f6e
Create Date: 2018-10-24 21:14:48.590238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b245668c166a'
down_revision = 'b01de4fa3f6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.String(length=30), nullable=False),
    sa.Column('nickname', sa.String(length=10), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('content', sa.String(length=500), nullable=False),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.Column('post_id', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
