"""empty message

Revision ID: d682232f0d8e
Revises:
Create Date: 2024-01-25 23:04:10.707460

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d682232f0d8e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "band_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=125), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("telegram_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram_id"),
    )
    op.create_table(
        "song_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=125), nullable=False),
        sa.Column("band_id", sa.Integer(), nullable=False),
        sa.Column("hits_count", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["band_id"], ["band_table.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "hit_counter_blacklist_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("song_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["song_id"], ["song_table.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["user_table.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "song_id", name="hit_counter_ff"),
    )
    op.create_table(
        "tab_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=125), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=False),
        sa.Column("song_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["song_id"], ["song_table.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_favorite_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("song_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["song_id"], ["song_table.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["user_table.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "song_id", name="user_favorite_song_ff"),
    )
    op.create_table(
        "verse_table",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=125), nullable=False),
        sa.Column("song_id", sa.Integer(), nullable=False),
        sa.Column("lyrics", sa.String(length=2000), nullable=True),
        sa.Column("chords", sa.String(length=1000), nullable=True),
        sa.ForeignKeyConstraint(["song_id"], ["song_table.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("verse_table")
    op.drop_table("user_favorite_table")
    op.drop_table("tab_table")
    op.drop_table("hit_counter_blacklist_table")
    op.drop_table("song_table")
    op.drop_table("user_table")
    op.drop_table("band_table")
    # ### end Alembic commands ###
