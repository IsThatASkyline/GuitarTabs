from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.db.models import BaseAlchemyModels


class BandMembers(BaseAlchemyModels):
    __tablename__ = "musician_band_table"
    __table_args__ = (UniqueConstraint('band_id', 'musician_id', name='musician_band_ff'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    band_id: Mapped[int] = mapped_column(
        ForeignKey("band_table.id", ondelete="CASCADE"), nullable=False
    )
    musician_id: Mapped[int] = mapped_column(
        ForeignKey("musician_table.id", ondelete="CASCADE"), nullable=False
    )


class UserFavorite(BaseAlchemyModels):
    __tablename__ = "user_favorite_table"
    __table_args__ = (UniqueConstraint('user_id', 'song_id', name='user_favorite_song_ff'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_table.id", ondelete="CASCADE"), nullable=False
    )
    song_id: Mapped[int] = mapped_column(
        ForeignKey("song_table.id", ondelete="CASCADE"), nullable=False
    )
