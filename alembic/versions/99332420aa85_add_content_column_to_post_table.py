"""add content column to post table

Revision ID: 99332420aa85
Revises: 66c0c9f8b231
Create Date: 2022-12-07 13:03:30.012798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99332420aa85'
down_revision = '66c0c9f8b231'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
