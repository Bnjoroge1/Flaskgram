"""added comment and savedposts table

Revision ID: 77c2ea850143
Revises: be681f355ce5
Create Date: 2020-08-31 21:58:24.089716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77c2ea850143'
down_revision = 'be681f355ce5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('saved_posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_saved', sa.DateTime(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_saved_posts_date_saved'), 'saved_posts', ['date_saved'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_saved_posts_date_saved'), table_name='saved_posts')
    op.drop_table('saved_posts')
    op.drop_table('comment')
    # ### end Alembic commands ###