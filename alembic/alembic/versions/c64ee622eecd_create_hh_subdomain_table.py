"""create hh_subdomain table

Revision ID: c64ee622eecd
Revises: 64d91a523884
Create Date: 2019-04-21 00:25:06.808599

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import relationship

# revision identifiers, used by Alembic.
revision = 'c64ee622eecd'
down_revision = '64d91a523884'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'hh_subdomain',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('id_domain', sa.Integer, primary_key=True),
        sa.Column('name', sa.Unicode(200), nullable=False),
        hh_domain=relationship("hh_domain", backref="hh_subdomain", cascade="save-update, merge, delete",
                               primaryjoin='hh_domain.id==hh_subdomain.id_domain'),

    )



def downgrade():
    pass
