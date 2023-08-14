"""test

Revision ID: 38898d28eb7d
Revises: 
Create Date: 2023-08-11 02:23:55.989253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38898d28eb7d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable = False),
        sa.Column('title', sa. String(), nullable = True),
        sa.Column('content', sa. String(), nullable = True),
        sa.Column('category', sa. String(), nullable = True),
        sa.Column('image', sa. String(), nullable = True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')

    )


def downgrade() -> None:
    op.drop_table('posts')
