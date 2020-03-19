"""create tasks table

Revision ID: 8848c49e2c26
Revises: 
Create Date: 2020-03-17 18:59:24.527035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8848c49e2c26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tasks_manager',
        sa.Column('pid', sa.Integer, primary_key=True),
        sa.Column('id', sa.String),
        sa.Column('title', sa.String),
        sa.Column('source', sa.String),
        sa.Column('destiny', sa.String),
        sa.Column('fails', sa.Boolean),
        sa.Column('processing', sa.Boolean),
        sa.Column('error', sa.String),
    )


def downgrade():
    op.drop_table('tasks_manager')
