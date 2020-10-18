"""added rq workers

Revision ID: b958d36d5f1a
Revises: 7a1adf24c578
Create Date: 2020-10-10 20:45:27.254682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b958d36d5f1a'
down_revision = '7a1adf24c578'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('complete', sa.Boolean(), nullable=True))
    op.add_column('task', sa.Column('description', sa.String(length=50), nullable=True))
    op.add_column('task', sa.Column('name', sa.String(length=20), nullable=False))
    op.add_column('task', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'user_id')
    op.drop_column('task', 'name')
    op.drop_column('task', 'description')
    op.drop_column('task', 'complete')
    # ### end Alembic commands ###
