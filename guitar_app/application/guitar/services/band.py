from guitar_app.application.guitar.dto import (
    BandDTO,
    CreateBandDTO,
    FullBandDTO,
    UpdateBandDTO,
)
from guitar_app.application.guitar.usecases import (
    CreateBand,
    DeleteBand,
    GetBandById,
    GetBands,
    UpdateBand,
)
from guitar_app.infrastructure.db.uow import UnitOfWork


class BandServices:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_band(self, band_dto: CreateBandDTO) -> BandDTO:
        async with self.uow:
            band = await CreateBand(self.uow)(band_dto)
            await self.uow.commit()
            return band

    async def get_all_bands(self) -> list[BandDTO]:
        return await GetBands(self.uow)()

    async def get_band_by_id(self, id_: int) -> FullBandDTO:
        return await GetBandById(self.uow)(id_)

    async def update_band(self, update_band_dto: UpdateBandDTO) -> FullBandDTO:
        async with self.uow:
            await UpdateBand(self.uow)(update_band_dto)
            await self.uow.commit()
            return await GetBandById(self.uow)(update_band_dto.id)

    async def delete_band(self, id_: int) -> None:
        async with self.uow:
            await DeleteBand(self.uow)(id_)
            await self.uow.commit()
