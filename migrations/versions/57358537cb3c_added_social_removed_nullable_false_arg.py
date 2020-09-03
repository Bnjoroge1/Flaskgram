"""added social removed nullable false arg

Revision ID: 57358537cb3c
Revises: 1cc3487a2d5b
Create Date: 2020-08-16 13:24:53.813224

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57358537cb3c'
down_revision = '1cc3487a2d5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('social', sa.String(length=64)))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.alter_column('image_file',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
        batch_op.create_unique_constraint(batch_op.f('uq_user_social'), ['social'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_social'), type_='unique')
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
        batch_op.alter_column('image_file',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
        batch_op.drop_column('social')

    # ### end Alembic commands ###
