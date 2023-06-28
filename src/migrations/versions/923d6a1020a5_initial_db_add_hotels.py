"""Initial migration

Revision ID: 923d6a1020a5
Revises:
Create Date: 2023-03-08 14:34:37.337959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '923d6a1020a5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'hotels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('services', sa.JSON(), nullable=True),
        sa.Column('rooms_quantity', sa.Integer(), nullable=False),
        sa.Column('image_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hotels')
    # ### end Alembic commands ###
