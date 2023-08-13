from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.guitarapp.dto import SongDTO, FullSongDTO, BaseVerseDTO
from src.infrastructure.db.models.base import BaseAlchemyModels


class Song(BaseAlchemyModels):
    __tablename__ = "song_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(125), nullable=False)
    band_id: Mapped[int] = mapped_column(ForeignKey("band_table.id", ondelete="CASCADE"), nullable=False)

    verses: Mapped["Verse"] = relationship()
    band: Mapped["Band"] = relationship(back_populates="songs")
    in_favorites: Mapped["User"] = relationship(secondary='user_favorite_table', back_populates="favorites")

    # V C V C B C V C
    #        Song
    #        Verse
    #   Lyrics   Chords
    #

    def to_dto(self) -> SongDTO:
        return SongDTO(
            id=self.id,
            title=self.title,
            band_id=self.band_id,
        )

    def to_full_dto(self, verses: BaseVerseDTO | None = None) -> FullSongDTO:
        return FullSongDTO(
            id=self.id,
            title=self.title,
            band_id=self.band_id,
            verses=verses
        )
