"""create cian table

Revision ID: f6d320ce8feb
Revises: 
Create Date: 2019-04-20 22:10:46.799778

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer, ForeignKey
# revision identifiers, used by Alembic.
revision = 'f6d320ce8feb'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'cian',
        sa.Column('id', sa.Integer, primary_key=True,  autoincrement=False),
        sa.Column('count_rooms', sa.Integer, nullable=False),
        sa.Column('id_station', sa.Integer, ForeignKey("station.id", ondelete="CASCADE"), nullable=False),
        sa.Column('price', sa.Numeric),
        sa.Column('floor', sa.Unicode(200)),
        sa.Column('square', sa.Numeric),
        sa.Column('price_sq', sa.Numeric),
        sa.Column('adress', sa.Unicode(200))
    #     station=relationship("station", backref="cian", cascade="save-update, merge, delete",
    #                          primaryjoin='station.id==cian.id_station'),
    #
    )
    pass
def downgrade():
    pass
