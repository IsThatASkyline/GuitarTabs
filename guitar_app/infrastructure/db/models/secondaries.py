from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from guitar_app.infrastructure.db.models import BaseAlchemyModels


class UserFavorite(BaseAlchemyModels):
    __tablename__ = "user_favorite_table"
    __table_args__ = (UniqueConstraint("user_id", "song_id", name="user_favorite_song_ff"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_table.id", ondelete="CASCADE"), nullable=False
    )
    song_id: Mapped[int] = mapped_column(
        ForeignKey("song_table.id", ondelete="CASCADE"), nullable=False
    )
