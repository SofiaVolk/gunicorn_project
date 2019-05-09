"""create yola_user

Revision ID: 862a0720c655
Revises: 6196e2012620
Create Date: 2019-05-05 22:34:13.910468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '862a0720c655'
down_revision = '6196e2012620'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'youla_user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Unicode(1000)),
        sa.Column('descrirption', sa.Unicode(1000)),
        sa.Column('product_id', sa.Unicode(1000)),
        sa.Column('category_id', sa.Unicode(1000)),
        sa.Column('subcategory_id', sa.Unicode(1000)),
        sa.Column('properties', sa.Unicode(1000)),
        sa.Column('image_links', sa.Unicode(1000)),
    )

def downgrade():
    pass
