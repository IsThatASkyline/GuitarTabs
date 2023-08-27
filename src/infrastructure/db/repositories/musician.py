from sqlalchemy.ext.asyncio import AsyncSession
from src.application.guitarapp.dto import CreateMusicianDTO, MusicianDTO
from src.infrastructure.db.models import Musician
from src.infrastructure.db.repositories.base import BaseRepository


class MusicianRepository(BaseRepository[Musician]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Musician, session)

    async def create_obj(self, musician_dto: CreateMusicianDTO) -> MusicianDTO:
        musician = Musician(
            first_name=musician_dto.first_name,
            last_name=musician_dto.last_name,
        )
        self.session.add(musician)
        await self.session.flush()
        return musician.to_dto()

    async def get_by_id(self, id_: int) -> MusicianDTO:
        musician = await super().get_by_id(id_)
        return musician.to_dto() if musician else None

    async def get_all(self) -> list[MusicianDTO]:
        musicians = await super().get_all()
        return [musician.to_dto() for musician in musicians] if musicians else None

    async def update_obj(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def delete_obj(self, id_: int):
        await super().delete_obj(id_)
