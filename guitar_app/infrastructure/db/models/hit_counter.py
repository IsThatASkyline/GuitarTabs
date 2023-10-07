from sqlalchemy import ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
import datetime

from guitar_app.application.guitar.dto import HitDTO
from guitar_app.infrastructure.db.models import BaseAlchemyModels


class HitCounterBlacklist(BaseAlchemyModels):
    __tablename__ = "hit_counter_blacklist_table"
    __table_args__ = (UniqueConstraint("user_id", "song_id", name="hit_counter_ff"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    song_id: Mapped[int] = mapped_column(
        ForeignKey("song_table.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_table.id", ondelete="CASCADE"), nullable=False
    )
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def to_dto(self) -> HitDTO:
        return HitDTO(
            id=self.id,
            song_id=self.song_id,
            user_id=self.user_id,
            created_at=self.created_date
        )
