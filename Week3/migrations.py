from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'authors',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=100), nullable=False, unique=True)
    )

    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False, unique=True)
    )

    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('isbn', sa.String(length=20), nullable=False, unique=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), sa.ForeignKey('authors.id')),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.id'))
    )


def downgrade():
    op.drop_table('books')
    op.drop_table('categories')
    op.drop_table('authors')
