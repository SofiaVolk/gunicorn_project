"""create hh_company table

Revision ID: 64d91a523884
Revises:
Create Date: 2019-04-20 23:43:20.687820

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64d91a523884'
down_revision = ''
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'hh_company',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(200)),

    )


def downgrade():
    pass
