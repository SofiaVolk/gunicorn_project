"""create vacancy_user table

Revision ID: d0ca878d320b
Revises: 229430c9da26
Create Date: 2019-04-21 01:30:05.959175

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey

# revision identifiers, used by Alembic.
revision = 'd0ca878d320b'
down_revision = '229430c9da26'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'vacancy_user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('id_company', sa.Integer, ForeignKey("hh_company.id", ondelete="CASCADE"), nullable=False),
        sa.Column('id_station', sa.Integer, ForeignKey("station.id", ondelete="CASCADE"), nullable=False),
        sa.Column('salary_min', sa.Numeric),
        sa.Column('salary_max', sa.Numeric),
        sa.Column('id_curency', sa.Integer, ForeignKey("curency.id", ondelete="CASCADE"), nullable=False),
        sa.Column('id_subdomain', sa.Integer, ForeignKey("hh_subdomain.id", ondelete="CASCADE"), nullable=False),
        sa.Column('adress', sa.Unicode(200)),
        # hh_company=relationship("hh_company", backref="vacancy_user", cascade="save-update, merge, delete",
        #                         primaryjoin='hh_company.id==vacancy_user.id_company'
        #                         ),
        # curency=relationship("curency", backref="vacancy_user", cascade="save-update, merge, delete",
        #                      primaryjoin='curency.id==vacancy_user.id_curency'
        #                      ),
        # # hh_sheldule = relationship("hh_sheldule", backref="vacancy_user", cascade="save-update, merge, delete",
        # #                               primaryjoin='hh_sheldule.id==vacancy_user.id_scheldule'),
        # hh_subdomain=relationship("hh_subdomain", backref="vacancy_user", cascade="save-update, merge, delete",
        #                           primaryjoin='hh_subdomain.id==vacancy_user.id_subdomain'),
        # station=relationship("station", backref="vacancy_user", cascade="save-update, merge, delete",
        #                      primaryjoin='station.id ==vacancy_user.id_station'),

    )


def downgrade():
    pass
