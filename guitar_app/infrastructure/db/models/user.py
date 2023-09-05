from sqlalchemy.orm import Mapped, mapped_column, relationship

from guitar_app.application.guitar.dto import UserDTO
from guitar_app.infrastructure.db.models import BaseAlchemyModels


class User(BaseAlchemyModels):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    telegram_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    favorites: Mapped["Song"] = relationship(
        secondary="user_favorite_table", back_populates="in_favorites"
    )

    def to_dto(self) -> UserDTO:
        return UserDTO(
            telegram_id=self.telegram_id,
            username=self.username,
        )
