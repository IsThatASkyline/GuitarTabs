from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload,selectinload

from src.domain.guitarapp.dto import CreateBandDTO, UpdateMusicianBandDTO, FullBandDTO, BandDTO
from src.infrastructure.db.models import Band, BandMembers, Musician, Song
from src.infrastructure.db.repositories.base import BaseRepository


class BandRepository(BaseRepository[Band]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Band, session)

    async def create_obj(self, band_dto: CreateBandDTO) -> BandDTO:
        band = Band(
            title=band_dto.title,
        )
        self.session.add(band)
        await self.session.flush()
        return band

    async def get_by_id(self, id_: int) -> FullBandDTO:
        query = select(Band).options(joinedload(Band.songs), joinedload(Band.members)).where(Band.id == id_)
        band = (await self._session.execute(query)).unique().scalar_one_or_none()

        return band.to_full_dto() if band else None

    async def get_all(self) -> list[BandDTO]:
        bands = await super().get_all()
        return [band.to_dto() for band in bands] if bands else None

    async def update_obj(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def delete_obj(self, id_: int):
        await super().delete_obj(id_)
