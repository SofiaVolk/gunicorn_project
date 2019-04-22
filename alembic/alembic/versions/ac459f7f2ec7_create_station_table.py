"""create station table

Revision ID: ac459f7f2ec7
Revises: f6d320ce8feb
Create Date: 2019-04-20 23:29:13.951630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac459f7f2ec7'
down_revision = 'f6d320ce8feb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'station',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(200), nullable=False),
    )


def downgrade():
    pass
