"""Add columns to issues table

Revision ID: 0f92b1e2efd8
Revises: 2b3b41bcd5c7
Create Date: 2021-08-10 11:46:26.606082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f92b1e2efd8'
down_revision = '2b3b41bcd5c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('issues', sa.Column('IssueType', sa.String(), nullable=True))
    op.add_column('issues', sa.Column('Status', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('issues', 'Status')
    op.drop_column('issues', 'IssueType')
    # ### end Alembic commands ###
