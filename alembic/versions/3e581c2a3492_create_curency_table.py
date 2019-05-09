"""create curency table

Revision ID: 3e581c2a3492
Revises:
Create Date: 2019-04-21 01:23:38.576279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e581c2a3492'
down_revision = ''
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'curency',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(200), nullable=False),
    )



def downgrade():
    pass
