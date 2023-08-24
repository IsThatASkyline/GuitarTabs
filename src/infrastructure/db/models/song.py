from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.guitarapp.dto import SongDTO, FullSongDTO, BaseVerseDTO
from src.infrastructure.db.models.base import BaseAlchemyModels


class Song(BaseAlchemyModels):
    __tablename__ = "song_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(125), nullable=False)
    band_id: Mapped[int] = mapped_column(ForeignKey("band_table.id", ondelete="CASCADE"), nullable=False)

    verses: Mapped[list["Verse"]] = relationship()
    band: Mapped["Band"] = relationship(back_populates="songs")
    in_favorites: Mapped["User"] = relationship(secondary='user_favorite_table', back_populates="favorites")

    def to_dto(self) -> SongDTO:
        return SongDTO(
            id=self.id,
            title=self.title,
            band=self.band,
        )

    def to_full_dto(self) -> FullSongDTO:
        return FullSongDTO(
            id=self.id,
            title=self.title,
            band=self.band,
            verses=self.verses
        )
