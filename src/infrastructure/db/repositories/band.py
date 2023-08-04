from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.guitarapp.dto import CreateBandDTO, UpdateMusicianBandDTO, FullBandDTO
from src.infrastructure.db.models import Band, MusicianBandTable
from src.infrastructure.db.repositories.base import BaseRepository


class BandRepository(BaseRepository[Band]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Band, session)

    async def create_band(self, band_dto: CreateBandDTO) -> FullBandDTO:
        band = Band(
            title=band_dto.title,
        )
        self.session.add(band)
        await self.session.flush()
        return band.to_full_dto()

    async def get_band_by_id(self, id_: int) -> FullBandDTO:
        band = await super().get_by_id(id_)
        return band.to_full_dto() if band else None

    async def get_all_bands(self) -> list[FullBandDTO]:
        bands = await super().get_all()
        return [band.to_full_dto() for band in bands] if bands else None

    async def update_band(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def add_musician_to_band(self, musician_dto: UpdateMusicianBandDTO) -> None:
        musician = MusicianBandTable(**musician_dto.dict())
        self.session.add(musician)

    async def delete_band(self, id_: int):
        await super().delete_obj(id_)
