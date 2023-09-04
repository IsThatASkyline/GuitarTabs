from guitar_app.application.common.usecases.base import BaseUseCase
from guitar_app.application.guitar.dto import MusicianDTO, CreateMusicianDTO, UpdateMusicianDTO
from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.application.guitar.exceptions import MusicianNotExists


class MusicianUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)


class GetMusicianById(MusicianUseCase):
    async def __call__(self, id_: int) -> MusicianDTO:
        if musician := await self.uow.app_holder.musician_repo.get_by_id(id_):
            return musician
        raise MusicianNotExists


class CreateMusician(MusicianUseCase):
    async def __call__(self, musician_dto: CreateMusicianDTO) -> MusicianDTO:
        return await self.uow.app_holder.musician_repo.create_obj(musician_dto)


class GetMusicians(MusicianUseCase):
    async def __call__(self) -> list[MusicianDTO]:
        return await self.uow.app_holder.musician_repo.get_all()


class UpdateMusician(MusicianUseCase):
    async def __call__(self, musician_update_dto: UpdateMusicianDTO) -> None:
        if await self.uow.app_holder.musician_repo.get_by_id(musician_update_dto.id):
            await self.uow.app_holder.musician_repo.update_obj(
                musician_update_dto.id,
                **musician_update_dto.dict(exclude_none=True, exclude=set("id")),
            )
            return
        else:
            raise MusicianNotExists


class DeleteMusician(MusicianUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.musician_repo.get_by_id(id_):
            await self.uow.app_holder.musician_repo.delete_obj(id_)
            return
        raise MusicianNotExists
