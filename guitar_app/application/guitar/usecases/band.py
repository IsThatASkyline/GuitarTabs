from guitar_app.application.common.usecases.base import BaseUseCase
from guitar_app.application.guitar.dto import FullBandDTO, CreateBandDTO, BandDTO, UpdateBandDTO, UpdateMusicianBandDTO
from guitar_app.infrastructure.db.uow import AbstractUnitOfWork
from guitar_app.application.guitar.exceptions import BandNotExists, MusicianNotExists


class BandUseCase(BaseUseCase):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        super().__init__(uow)


class GetBandById(BandUseCase):
    async def __call__(self, id_: int) -> FullBandDTO:
        if band := await self.uow.app_holder.band_repo.get(id_):
            return band
        raise BandNotExists


class CreateBand(BandUseCase):
    async def __call__(self, band_dto: CreateBandDTO) -> FullBandDTO:
        return await self.uow.app_holder.band_repo.add(band_dto)


class GetBands(BandUseCase):
    async def __call__(self) -> list[BandDTO]:
        return await self.uow.app_holder.band_repo.list()


class UpdateBand(BandUseCase):
    async def __call__(self, band_update_dto: UpdateBandDTO) -> None:
        if await self.uow.app_holder.band_repo.get(band_update_dto.id):
            await self.uow.app_holder.band_repo.update(
                band_update_dto.id,
                **band_update_dto.dict(exclude_none=True, exclude=set("id")),
            )
            return
        raise BandNotExists


class UpdateMusicianBand(BandUseCase):
    async def __call__(self, musician_band_update_dto: UpdateMusicianBandDTO) -> None:
        if await self.uow.app_holder.band_repo.get(musician_band_update_dto.band_id):
            if await self.uow.app_holder.musician_repo.get(musician_band_update_dto.musician_id):
                return await self.uow.app_holder.band_members_repo.add(musician_band_update_dto)
            raise MusicianNotExists
        raise BandNotExists


class DeleteBand(BandUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.band_repo.get(id_):
            await self.uow.app_holder.band_repo.delete(id_)
            return
        raise BandNotExists
