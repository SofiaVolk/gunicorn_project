"""create foreign key

Revision ID: dd397e7a7cb7
Revises: f63cfc2c1534
Create Date: 2019-05-05 22:06:23.635242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd397e7a7cb7'
down_revision = 'f63cfc2c1534'
branch_labels = None
depends_on = None

def upgrade():
    op.create_foreign_key(
        "fk_vacancy_domain", "hh_vacancy",
        "hh_domain", ["id_domain"], ["id"],ondelete="CASCADE",onupdate='CASCADE')
    op.create_foreign_key(
        "fk_vacancy_company", "hh_vacancy",
        "hh_company", ["id_company"], ["id"],ondelete="CASCADE",onupdate='CASCADE')
    op.create_foreign_key(
        "fk_vacancy_curency", "hh_vacancy",
        "curency", ["id_curency"], ["id"],ondelete="CASCADE",onupdate='CASCADE')
    op.create_foreign_key(
        "fk_vacancy_station", "hh_vacancy",
        "station", ["id_station"], ["id"],ondelete="CASCADE",onupdate='CASCADE')
    #other
    op.create_foreign_key(
        "fk_vacancy_user_domain", "hh_vacancy_user",
        "hh_domain", ["id_domain"], ["id"],ondelete="CASCADE",onupdate='CASCADE')
    op.create_foreign_key(
        "fk_vacancy_user_company", "hh_vacancy_user",
        "hh_company", ["id_company"], ["id"],ondelete="CASCADE",onupdate='CASCADE')
    op.create_foreign_key(
        "fk_vacancy_user_curency", "hh_vacancy_user",
        "curency", ["id_curency"], ["id"],ondelete="CASCADE",onupdate='CASCADE')
    op.create_foreign_key(
        "fk_vacancy_user_station", "hh_vacancy_user",
        "station", ["id_station"], ["id"],ondelete="CASCADE",onupdate='CASCADE')

def downgrade():
    pass
