"""create cian_user table

Revision ID: 6c003c9c157b
Revises: d0ca878d320b
Create Date: 2019-04-21 01:30:22.256892

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey
# revision identifiers, used by Alembic.
revision = '6c003c9c157b'
down_revision = 'd0ca878d320b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cian_user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('count_rooms', sa.Integer, nullable=False),
        sa.Column('id_station', sa.Integer, ForeignKey("station.id", ondelete="CASCADE"), nullable=False),
        sa.Column('price', sa.Numeric),
        sa.Column('floor', sa.Unicode(200)),
        sa.Column('square', sa.Numeric),
        sa.Column('price_sq', sa.Numeric),
        sa.Column('adress', sa.Unicode(200)),
        # station=relationship("station", backref="cian_user", cascade="save-update, merge, delete",
        #                      primaryjoin='station.id==cian_user.id_station'),

    )


def downgrade():
    pass
