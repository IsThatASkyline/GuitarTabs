from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from guitar_app.src.infrastructure.db.models.base import BaseAlchemyModels


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
    # date_of_birth
    # date_of_birth

    # bands: Mapped["Band"] = relationship(back_populates="members", secondary='musician_band_table')
