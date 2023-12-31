from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guitar_app.application.guitar.dto import BaseVerseDTO
from guitar_app.infrastructure.db.models import BaseAlchemyModels


class Verse(BaseAlchemyModels):
    __tablename__ = "verse_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(125), nullable=False)
    song_id: Mapped[int] = mapped_column(
        ForeignKey("song_table.id", ondelete="CASCADE"), nullable=False
    )

    song: Mapped["Song"] = relationship(back_populates="verses")

    lyrics: Mapped[str] = mapped_column(String(2000), nullable=True)
    chords: Mapped[str] = mapped_column(String(1000), nullable=True)

    def to_dto(self) -> BaseVerseDTO:
        return BaseVerseDTO(
            title=self.title,
            lyrics=self.lyrics,
            chords=self.chords,
        )
