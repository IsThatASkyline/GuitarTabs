"""empty message

Revision ID: 8d3a5d224eae
Revises: 6ad7f3a6669d
Create Date: 2023-08-06 22:12:05.034970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d3a5d224eae'
down_revision = '6ad7f3a6669d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song_table', sa.Column('band_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'song_table', 'band_table', ['band_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'song_table', type_='foreignkey')
    op.drop_column('song_table', 'band_id')
    # ### end Alembic commands ###
