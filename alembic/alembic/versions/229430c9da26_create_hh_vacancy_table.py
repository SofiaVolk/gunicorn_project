"""create hh_vacancy table

Revision ID: 229430c9da26
Revises: 3e581c2a3492
Create Date: 2019-04-21 01:25:15.392775

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from sqlalchemy import Integer, ForeignKey
# revision identifiers, used by Alembic.
revision = '229430c9da26'
down_revision = '3e581c2a3492'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'hh_vacancy',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=False),
        sa.Column('id_company', sa.Integer, ForeignKey("hh_company.id", ondelete="CASCADE"), nullable=False),
        sa.Column('id_station', sa.Integer, ForeignKey("station.id", ondelete="CASCADE"), nullable=False),
        sa.Column('salary_min', sa.Numeric),
        sa.Column('salary_max', sa.Numeric),
        sa.Column('id_curency', sa.Integer, ForeignKey("curency.id", ondelete="CASCADE"), nullable=False),
        sa.Column('id_subdomain', sa.Integer, ForeignKey("hh_subdomain.id", ondelete="CASCADE"), nullable=False),
        sa.Column('adress', sa.Unicode(200)))
    #     hh_company=relationship("hh_company", backref="hh_vacancy", cascade="save-update, merge, delete",
    #                                primaryjoin='hh_company.id==hh_vacancy.id_company'
    #                                ),
    # curency = relationship("curency", backref="hh_vacancy", cascade="save-update, merge, delete",
    #                           primaryjoin='curency.id==hh_vacancy.id_curency'
    #                           ),
    # # hh_sheldule = relationship("hh_sheldule", backref="hh_vacancy", cascade="save-update, merge, delete",
    # #                               primaryjoin='hh_sheldule.id==hh_vacancy.id_scheldule'),
    # hh_subdomain = relationship("hh_subdomain", backref="hh_vacancy", cascade="save-update, merge, delete",
    #                               primaryjoin='hh_subdomain.id==hh_vacancy.id_subdomain'
    #                             ),
    # station = relationship("station", backref="hh_vacancy", cascade="save-update, merge, delete"
    #                         , primaryjoin='station.id ==hh_vacancy.id_station'
    #                        )
    #
    # )



def downgrade():
    pass
