from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from guitar_app.application.guitar.dto import TabDTO
from guitar_app.infrastructure.db.models import BaseAlchemyModels


class Tab(BaseAlchemyModels):
    __tablename__ = "tab_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(125), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    song_id: Mapped[int] = mapped_column(
        ForeignKey("song_table.id", ondelete="CASCADE"), nullable=False
    )

    song: Mapped["Song"] = relationship(back_populates="tabs")

    def to_dto(self) -> TabDTO:
        return TabDTO(
            id=self.id,
            title=self.title,
            image_url=self.image_url
        )
