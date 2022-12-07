"""add foreign key to post table

Revision ID: 97c4cb6686c5
Revises: 770247b7aecb
Create Date: 2022-12-07 13:20:10.763627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97c4cb6686c5'
down_revision = '770247b7aecb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fkey", source_table="posts", referent_table="users", local_cols=["user_id"], 
        remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', column_name='user_id')
    pass
