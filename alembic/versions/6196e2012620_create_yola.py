"""create yola

Revision ID: 6196e2012620
Revises: dd397e7a7cb7
Create Date: 2019-05-05 22:29:28.841233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6196e2012620'
down_revision = 'dd397e7a7cb7'
branch_labels = None
depends_on = None

#title,descrirption,product_id,category_id,subcategory_id,properties,image_links
def upgrade():
    op.create_table(
        'youla',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Unicode(1000)),
        sa.Column('descrirption', sa.Unicode(10000)),
        sa.Column('product_id', sa.Unicode(1000)),
        sa.Column('category_id', sa.Unicode(1000)),
        sa.Column('subcategory_id', sa.Unicode(1000)),
        sa.Column('properties', sa.Unicode(1000)),
        sa.Column('image_links', sa.Unicode(1000)),
    )


def downgrade():
    pass
