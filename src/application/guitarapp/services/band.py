from src.application.guitarapp.dto import CreateBandDTO, BandDTO, UpdateBandDTO, FullBandDTO, UpdateMusicianBandDTO
from src.application.guitarapp.usecases import CreateBand, GetBandById, GetBands, UpdateBand, UpdateMusicianBand, DeleteBand
from src.infrastructure.db.uow import UnitOfWork


class BandServices:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_band(self, band_dto: CreateBandDTO) -> FullBandDTO:
        async with self.uow:
            band = await CreateBand(self.uow)(band_dto)
            await self.uow.commit()
            return await GetBandById(self.uow)(band.id)

    async def get_all_bands(self) -> list[BandDTO]:
        return await GetBands(self.uow)()

    async def get_band_by_id(self, id_: int) -> FullBandDTO:
        return await GetBandById(self.uow)(id_)

    async def update_band(self, update_band_dto: UpdateBandDTO) -> FullBandDTO:
        async with self.uow:
            await UpdateBand(self.uow)(update_band_dto)
            await self.uow.commit()
            return await GetBandById(self.uow)(update_band_dto.id)

    async def add_musician_to_band(self, update_musician_band_dto: UpdateMusicianBandDTO) -> FullBandDTO:
        async with self.uow:
            await UpdateMusicianBand(self.uow)(update_musician_band_dto)
            await self.uow.commit()
            return await GetBandById(self.uow)(update_musician_band_dto.band_id)

    async def delete_band(self, id_: int) -> None:
        async with self.uow:
            await DeleteBand(self.uow)(id_)
            await self.uow.commit()
