from src.domain.guitarapp.dto import CreateBandDTO, BandDTO, UpdateBandDTO, FullBandDTO, UpdateMusicianBandDTO
from src.domain.guitarapp.exceptions import BandNotExists, SmthWithAddingToBand
from src.domain.guitarapp.usecases import BandUseCase
from src.infrastructure.db.uow import UnitOfWork


class GetBandById(BandUseCase):
    async def __call__(self, id_: int) -> FullBandDTO:
        if band := await self.uow.app_holder.band_repo.get_band_by_id(id_):
            return band
        raise BandNotExists


class CreateBand(BandUseCase):
    async def __call__(self, band_dto: CreateBandDTO) -> FullBandDTO:
        band = await self.uow.app_holder.band_repo.create_band(band_dto)
        await self.uow.commit()
        return band


class GetBands(BandUseCase):
    async def __call__(self) -> list[BandDTO]:
        bands = await self.uow.app_holder.band_repo.get_all_bands()
        return bands


class UpdateBand(BandUseCase):
    async def __call__(self, band_update_dto: UpdateBandDTO) -> None:
        await self.uow.app_holder.band_repo.update_band(
            band_update_dto.id,
            **band_update_dto.dict(exclude_none=True, exclude=set("id")),
        )
        await self.uow.commit()


class UpdateMusicianBand(BandUseCase):
    async def __call__(self, musician_band_update_dto: UpdateMusicianBandDTO) -> None:
        if await self.uow.app_holder.band_repo.get_band_by_id(musician_band_update_dto.band_id) and \
                await self.uow.app_holder.musician_repo.get_musician_by_id(musician_band_update_dto.musician_id):
            await self.uow.app_holder.band_repo.add_musician_to_band(musician_band_update_dto)
            await self.uow.commit()
            return
        raise SmthWithAddingToBand


class DeleteBand(BandUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.band_repo.get_band_by_id(id_):
            await self.uow.app_holder.band_repo.delete_band(id_)
            await self.uow.commit()
            return
        raise BandNotExists


class BandServices:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_band(self, user_dto: CreateBandDTO) -> FullBandDTO:
        return await CreateBand(self.uow)(user_dto)

    async def get_all_bands(self) -> list[BandDTO]:
        return await GetBands(self.uow)()

    async def get_band_by_id(self, id_: int) -> FullBandDTO:
        return await GetBandById(self.uow)(id_)

    async def update_band(self, update_band_dto: UpdateBandDTO) -> FullBandDTO:
        await UpdateBand(self.uow)(update_band_dto)
        return await GetBandById(self.uow)(update_band_dto.id)

    async def add_musician_to_band(self, update_musician_dto: UpdateMusicianBandDTO) -> FullBandDTO:
        await UpdateMusicianBand(self.uow)(update_musician_dto)
        return await GetBandById(self.uow)(update_musician_dto.band_id)

    async def delete_band(self, id_: int) -> None:
        await DeleteBand(self.uow)(id_)
