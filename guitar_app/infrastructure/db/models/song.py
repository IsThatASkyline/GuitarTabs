from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guitar_app.application.guitar.dto import FullSongDTO, SongDTO
from guitar_app.infrastructure.db.models import BaseAlchemyModels


class Song(BaseAlchemyModels):
    __tablename__ = "song_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(125), nullable=False)
    band_id: Mapped[int] = mapped_column(
        ForeignKey("band_table.id", ondelete="CASCADE"), nullable=False
    )

    verses: Mapped[list["Verse"]] = relationship()
    band: Mapped["Band"] = relationship(back_populates="songs")
    in_favorites: Mapped["User"] = relationship(
        secondary="user_favorite_table", back_populates="favorites"
    )

    def to_dto(self) -> SongDTO:
        return SongDTO(
            id=self.id,
            title=self.title,
            band=self.band.to_dto(),
        )

    def to_full_dto(self) -> FullSongDTO:
        return FullSongDTO(
            id=self.id,
            title=self.title,
            band=self.band.to_dto(),
            verses=[verse.to_dto() for verse in self.verses],
        )
