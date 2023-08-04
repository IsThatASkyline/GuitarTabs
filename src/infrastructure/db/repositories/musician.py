from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.guitarapp.dto import CreateMusicianDTO, MusicianDTO
from src.infrastructure.db.models import Musician, MusicianBandTable
from src.infrastructure.db.repositories.base import BaseRepository


class MusicianRepository(BaseRepository[Musician]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Musician, session)

    async def create_musician(self, musician_dto: CreateMusicianDTO) -> MusicianDTO:
        musician = Musician(
            first_name=musician_dto.first_name,
            last_name=musician_dto.last_name,
        )
        self.session.add(musician)
        await self.session.flush()
        return musician.to_dto()

    async def get_musician_by_id(self, id_: int) -> MusicianDTO:
        musician = await super().get_by_id(id_)
        return musician.to_dto() if musician else None

    async def get_all_musicians(self) -> list[MusicianDTO]:
        musicians = await super().get_all()
        return [musician.to_dto() for musician in musicians] if musicians else None

    async def get_all_musicians_in_band(self, id_: int) -> list[MusicianDTO]:
        query = select(Musician).join(MusicianBandTable).where(MusicianBandTable.band_id == id_)
        musicians = (await self.session.execute(query)).scalars().all()
        return [musician.to_dto() for musician in musicians] if musicians else None

    async def update_musician(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def delete_musician(self, id_: int):
        await super().delete_obj(id_)
