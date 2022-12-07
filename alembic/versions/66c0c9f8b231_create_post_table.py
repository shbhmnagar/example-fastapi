"""create post table

Revision ID: 66c0c9f8b231
Revises: 
Create Date: 2022-12-07 12:48:57.276017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66c0c9f8b231'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
