from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guitar_app.application.guitar.dto import BandDTO, FullBandDTO
from guitar_app.infrastructure.db.models import BaseAlchemyModels


class Band(BaseAlchemyModels):
    __tablename__ = "band_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(125),
        nullable=False,
    )
    songs: Mapped[list["Song"]] = relationship(back_populates="band")

    def to_dto(self) -> BandDTO:
        return BandDTO(
            id=self.id,
            title=self.title,
        )

    def to_full_dto(self) -> FullBandDTO:
        return FullBandDTO(
            id=self.id,
            title=self.title,
            songs=[song.to_dto() for song in self.songs],
        )
