"""empty message

Revision ID: ba6fbc391fb8
Revises: 88afc3b6bbe5
Create Date: 2024-12-03 00:05:20.297202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba6fbc391fb8'
down_revision = '88afc3b6bbe5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.drop_column('films')
        batch_op.drop_column('homeworld')

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_column('films')

    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.drop_column('length')
        batch_op.drop_column('crew')
        batch_op.drop_column('films')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('films', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('crew', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('length', sa.VARCHAR(), autoincrement=False, nullable=False))

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('films', sa.VARCHAR(), autoincrement=False, nullable=False))

    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('homeworld', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('films', sa.VARCHAR(), autoincrement=False, nullable=False))

    # ### end Alembic commands ###