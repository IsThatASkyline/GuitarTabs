from sqlalchemy.ext.asyncio import AsyncSession
from guitar_app.application.guitar.dto import CreateMusicianDTO, MusicianDTO
from guitar_app.infrastructure.db.models import Musician
from guitar_app.infrastructure.db.repositories.base import BaseRepository


class MusicianRepository(BaseRepository[Musician]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Musician, session)

    async def add(self, musician_dto: CreateMusicianDTO) -> MusicianDTO:
        musician = Musician(
            first_name=musician_dto.first_name,
            last_name=musician_dto.last_name,
        )
        self.session.add(musician)
        await self.session.flush()
        return musician.to_dto()

    async def get(self, id_: int) -> MusicianDTO:
        musician: Musician = await super().get(id_)
        return musician.to_dto() if musician else None

    async def list(self) -> list[MusicianDTO]:
        musicians = await super().list()
        return [musician.to_dto() for musician in musicians] if musicians else None

    async def update(self, id_: int, **kwargs) -> None:
        await super().update(id_, **kwargs)

    async def delete(self, id_: int):
        await super().delete(id_)
