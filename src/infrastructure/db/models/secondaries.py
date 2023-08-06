from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models.base import BaseAlchemyModels


class MusicianBandLink(BaseAlchemyModels):
    __tablename__ = "musician_band_table"
    __table_args__ = (UniqueConstraint('band_id', 'musician_id', name='musician_band_ff'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    band_id: Mapped[int] = mapped_column(
        ForeignKey("band_table.id", ondelete="CASCADE"), nullable=False
    )
    musician_id: Mapped[int] = mapped_column(
        ForeignKey("musician_table.id", ondelete="CASCADE"), nullable=False
    )

