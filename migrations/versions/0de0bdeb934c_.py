"""empty message

Revision ID: 0de0bdeb934c
Revises: 8657c63989d3
Create Date: 2023-04-04 09:48:40.774185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0de0bdeb934c'
down_revision = '8657c63989d3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookmark', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_bookmark_status'), ['status'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bookmark', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_bookmark_status'))
        batch_op.drop_column('status')

    # ### end Alembic commands ###
