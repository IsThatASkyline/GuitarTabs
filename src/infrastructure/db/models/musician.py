from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.guitarapp.dto import MusicianDTO
from src.infrastructure.db.models.base import BaseAlchemyModels


class Musician(BaseAlchemyModels):
    __tablename__ = "musician_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(
        String(125),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(125),
        nullable=False,
    )
    bands: Mapped[list["Band"]] = relationship(back_populates="members", secondary='musician_band_table')

    def to_dto(self) -> MusicianDTO:
        return MusicianDTO(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
        )
