from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from guitar_app.application.guitar.dto import CreateBandDTO, FullBandDTO, BandDTO
from guitar_app.infrastructure.db.models import Band
from guitar_app.infrastructure.db.repositories.base import BaseRepository


class BandRepository(BaseRepository[Band]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Band, session)

    async def add(self, band_dto: CreateBandDTO) -> BandDTO:
        band = Band(
            title=band_dto.title,
        )
        self.session.add(band)
        await self.session.flush()
        return band.to_dto()

    async def get(self, id_: int) -> FullBandDTO:
        query = select(Band).options(joinedload(Band.songs), joinedload(Band.members)).where(Band.id == id_)
        band = (await self._session.execute(query)).unique().scalar_one_or_none()

        return band.to_full_dto() if band else None

    async def list(self) -> list[BandDTO]:
        bands = await super().list()
        return [band.to_dto() for band in bands] if bands else None

    async def update(self, id_: int, **kwargs) -> None:
        await super().update(id_, **kwargs)

    async def delete(self, id_: int):
        await super().delete(id_)
