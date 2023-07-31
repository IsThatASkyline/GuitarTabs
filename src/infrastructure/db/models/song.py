from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models.base import BaseAlchemyModels


class Song(BaseAlchemyModels):
    __tablename__ = "song_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(125),
        nullable=False,
    )
    lyrics: Mapped[str] = mapped_column(Text, nullable=False)
    band_id: Mapped[int] = mapped_column(
        ForeignKey("band_table.id", ondelete="CASCADE"), nullable=False
    )

    band: Mapped["Band"] = relationship(back_populates="songs")

    # tabs: Mapped[str] = mapped_column(Text, nullable=False)
    # Альбомы