from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.guitarapp.dto import FullBandDTO
from .musician import Musician
from src.infrastructure.db.models.base import BaseAlchemyModels


class Band(BaseAlchemyModels):
    __tablename__ = "band_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(125),
        nullable=False,
    )

    songs: Mapped["Song"] = relationship(back_populates="band", lazy='joined')
    members: Mapped["Musician"] = relationship(back_populates="bands", secondary='musician_band_table', lazy='selectin')

    # Альбомы
    # Дата основания
    # Дата распада

    def to_full_dto(self, members: list[Musician] | None = None) -> FullBandDTO:
        return FullBandDTO(
            id=self.id,
            title=self.title,
            members=members,
        )
