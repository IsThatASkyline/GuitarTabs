from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from guitar_app.application.guitar.dto import (
    CreateMusicianDTO,
    MusicianDTO,
    UpdateMusicianDTO,
)
from guitar_app.infrastructure.db.models import Musician
from guitar_app.infrastructure.db.repositories.base import BaseRepository


class MusicianRepository(BaseRepository[Musician]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Musician, session)

    async def add_musician(self, musician_dto: CreateMusicianDTO) -> MusicianDTO:
        musician = Musician(
            first_name=musician_dto.first_name,
            last_name=musician_dto.last_name,
        )
        self.session.add(musician)
        await self.session.flush()
        return musician.to_dto()

    async def get_musician(self, id_: int) -> MusicianDTO | None:
        musician: Musician = await super().get(id_)
        return musician.to_dto() if musician else None

    async def list_musicians(self) -> list[MusicianDTO] | None:
        musicians = (
            await self.session.execute(select(Musician).order_by(Musician.first_name))
        ).scalars()
        return [musician.to_dto() for musician in musicians] if musicians else None

    async def update_musician(self, musician_update_dto: UpdateMusicianDTO) -> None:
        await super().update(
            id_=musician_update_dto.id,
            first_name=musician_update_dto.first_name,
            last_name=musician_update_dto.last_name,
        )

    async def delete_musician(self, id_: int):
        await super().delete(id_)
