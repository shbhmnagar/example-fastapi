"""add users table

Revision ID: 770247b7aecb
Revises: 99332420aa85
Create Date: 2022-12-07 13:11:18.725202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '770247b7aecb'
down_revision = '99332420aa85'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')
