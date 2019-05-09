"""create hh_domain table

Revision ID: 229430c9da26
Revises:
Create Date: 2019-04-20 23:59:08.566430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '229430c9da26'
down_revision = ''
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'hh_domain',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(200), nullable=False),
    )


def downgrade():
    pass
