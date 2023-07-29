from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guitar_app.src.infrastructure.db.models.base import BaseAlchemyModels


class Band(BaseAlchemyModels):
    __tablename__ = "band_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(125),
        nullable=False,
    )
    # Альбомы
    # Дата основания
    # Дата распада
    members: Mapped["Musician"] = relationship(back_populates="bands", secondary='musician_band_table')
