"""create hh_vacancy table

Revision ID: 3aed7e422836
Revises:
Create Date: 2019-04-21 01:25:15.392775

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from sqlalchemy import Integer, ForeignKey
# revision identifiers, used by Alembic.
revision = '3aed7e422836'
down_revision = ''
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'hh_vacancy',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=False),
        sa.Column('title', sa.Unicode(200)),
        sa.Column('id_domain', sa.Integer),
        sa.Column('id_company', sa.Integer),
        sa.Column('description', sa.Unicode(10000)),
        sa.Column('salary_min', sa.Numeric),
        sa.Column('salary_max', sa.Numeric),
        sa.Column('id_curency', sa.Integer),
        sa.Column('id_station', sa.Integer)

    )





def downgrade():
    pass
