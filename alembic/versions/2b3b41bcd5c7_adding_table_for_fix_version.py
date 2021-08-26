"""Adding table for fix version

Revision ID: 2b3b41bcd5c7
Revises: 73435615430b
Create Date: 2021-08-10 09:21:01.127426

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b3b41bcd5c7'
down_revision = '73435615430b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fixversions',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Name', sa.String(), nullable=True),
    sa.Column('JiraId', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('Id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fixversions')
    # ### end Alembic commands ###
