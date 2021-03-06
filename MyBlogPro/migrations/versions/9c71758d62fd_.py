"""empty message

Revision ID: 9c71758d62fd
Revises: 44225a77c075
Create Date: 2019-06-23 14:41:47.969179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c71758d62fd'
down_revision = '44225a77c075'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sort', sa.Column('othername', sa.String(length=100), nullable=True))
    op.create_unique_constraint(None, 'sort', ['othername'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'sort', type_='unique')
    op.drop_column('sort', 'othername')
    # ### end Alembic commands ###
