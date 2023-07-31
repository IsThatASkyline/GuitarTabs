from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.guitarapp.dto import CreateBandDTO, UpdateMusicianBandDTO
from src.infrastructure.db.models import Band, MusicianBandTable
from src.infrastructure.db.repositories.base import BaseRepository


class BandRepository(BaseRepository[Band]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Band, session)

    async def create_band(self, band_dto: CreateBandDTO) -> Band:
        band = Band(
            title=band_dto.title,
        )
        self.session.add(band)
        return band

    async def get_band_by_id(self, id_: int) -> Band:
        return await super().get_by_id(id_)

    async def get_all_bands(self) -> list[Band]:
        return await super().get_all()

    async def update_band(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def add_musician_to_band(self, musician_dto: UpdateMusicianBandDTO) -> None:
        musician = MusicianBandTable(**musician_dto.dict())
        self.session.add(musician)
        return

    async def delete_band(self, id_: int):
        await super().delete_obj(id_)
