from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models.base import BaseAlchemyModels


class User(BaseAlchemyModels):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(125), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)

    password: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    favorites: Mapped["Song"] = relationship(secondary='user_favorite_table', back_populates='in_favorites')
