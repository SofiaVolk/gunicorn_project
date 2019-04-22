"""create hh_company table

Revision ID: e74da5685f88
Revises: ac459f7f2ec7
Create Date: 2019-04-20 23:43:20.687820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e74da5685f88'
down_revision = 'ac459f7f2ec7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'hh_company',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(200)),
        sa.Column('adress', sa.Unicode(200)),
    )


def downgrade():
    pass
