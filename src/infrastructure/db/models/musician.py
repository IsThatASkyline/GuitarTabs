from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    bands: Mapped["Band"] = relationship(back_populates="members", secondary='musician_band_table')
