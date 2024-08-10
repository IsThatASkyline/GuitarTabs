from guitar_app.application.common.usecases.base import BaseUseCase
from guitar_app.application.guitar.dto import (
    BandDTO,
    CreateBandDTO,
    FullBandDTO,
    UpdateBandDTO,
)
from guitar_app.application.guitar.exceptions import BandNotExists
from guitar_app.infrastructure.db.uow import UnitOfWork


class BandUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)


class GetBandById(BandUseCase):
    async def __call__(self, id_: int) -> FullBandDTO:
        if band := await self.uow.app_holder.band_repo.get_band(id_):
            return band
        raise BandNotExists


class CreateBand(BandUseCase):
    async def __call__(self, band_dto: CreateBandDTO) -> BandDTO:
        return await self.uow.app_holder.band_repo.add_band(band_dto)


class GetBands(BandUseCase):
    async def __call__(self) -> list[BandDTO]:
        return await self.uow.app_holder.band_repo.list_bands()


class UpdateBand(BandUseCase):
    async def __call__(self, band_update_dto: UpdateBandDTO) -> None:
        if await self.uow.app_holder.band_repo.get_band(band_update_dto.id):
            await self.uow.app_holder.band_repo.update_band(band_update_dto)
            return
        raise BandNotExists


class DeleteBand(BandUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.band_repo.get_band(id_):
            await self.uow.app_holder.band_repo.delete_band(id_)
            return
        raise BandNotExists
