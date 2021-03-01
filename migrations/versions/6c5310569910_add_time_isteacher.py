"""add_time_isteacher

Revision ID: 6c5310569910
Revises: ce35ec91e0e5
Create Date: 2021-03-01 00:04:51.809315

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c5310569910'
down_revision = 'ce35ec91e0e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('isteacher', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'time_created')
    op.drop_column('user', 'isteacher')
    # ### end Alembic commands ###