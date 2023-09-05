from guitar_app.application.common.usecases.base import BaseUseCase
from guitar_app.application.guitar.dto import (
    CreateMusicianDTO,
    MusicianDTO,
    UpdateMusicianDTO,
)
from guitar_app.application.guitar.exceptions import MusicianNotExists
from guitar_app.infrastructure.db.uow import UnitOfWork


class MusicianUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)


class GetMusicianById(MusicianUseCase):
    async def __call__(self, id_: int) -> MusicianDTO:
        if musician := await self.uow.app_holder.musician_repo.get_musician(id_):
            return musician
        raise MusicianNotExists


class CreateMusician(MusicianUseCase):
    async def __call__(self, musician_dto: CreateMusicianDTO) -> MusicianDTO:
        return await self.uow.app_holder.musician_repo.add_musician(musician_dto)


class GetMusicians(MusicianUseCase):
    async def __call__(self) -> list[MusicianDTO]:
        return await self.uow.app_holder.musician_repo.list_musicians()


class UpdateMusician(MusicianUseCase):
    async def __call__(self, musician_update_dto: UpdateMusicianDTO) -> None:
        if await self.uow.app_holder.musician_repo.get_musician(musician_update_dto.id):
            await self.uow.app_holder.musician_repo.update_musician(
                musician_update_dto.id,
                **musician_update_dto.dict(exclude_none=True, exclude=set("id")),
            )
            return
        else:
            raise MusicianNotExists


class DeleteMusician(MusicianUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.musician_repo.get_musician(id_):
            await self.uow.app_holder.musician_repo.delete_musician(id_)
            return
        raise MusicianNotExists
