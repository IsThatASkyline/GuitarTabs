from guitar_app.src.domain.guitarapp.dto.musician import CreateMusicianDTO, MusicianDTO, UpdateMusicianDTO
from guitar_app.src.domain.guitarapp.exceptions import MusicianNotExists
from guitar_app.src.domain.guitarapp.interfaces import MusicianUseCase
from guitar_app.src.infrastructure.db.uow import UnitOfWork


class GetMusicianById(MusicianUseCase):
    async def __call__(self, id_: int) -> MusicianDTO:
        if musician := await self.uow.app_holder.musician_repo.get_musician_by_id(id_):
            return musician
        raise MusicianNotExists


class CreateMusician(MusicianUseCase):
    async def __call__(self, musician_dto: CreateMusicianDTO) -> MusicianDTO:
        musician = await self.uow.app_holder.musician_repo.create_musician(musician_dto)
        await self.uow.commit()
        return musician


class GetMusicians(MusicianUseCase):
    async def __call__(self) -> list[MusicianDTO]:
        musicians = await self.uow.app_holder.musician_repo.get_all_musicians()
        return musicians


class UpdateMusician(MusicianUseCase):
    async def __call__(self, musician_update_dto: UpdateMusicianDTO) -> None:
        await self.uow.app_holder.musician_repo.update_musician(
            musician_update_dto.id,
            **musician_update_dto.dict(exclude_none=True, exclude=set("id")),
        )
        await self.uow.commit()


class DeleteMusician(MusicianUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.musician_repo.get_musician_by_id(id_):
            await self.uow.app_holder.musician_repo.delete_musician(id_)
            await self.uow.commit()
            return
        raise MusicianNotExists


class MusicianServices:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_musician(self, user_dto: CreateMusicianDTO) -> MusicianDTO:
        return await CreateMusician(self.uow)(user_dto)

    async def get_all_musicians(self) -> list[MusicianDTO]:
        return await GetMusicians(self.uow)()

    async def get_musician_by_id(self, id_: int) -> MusicianDTO:
        return await GetMusicianById(self.uow)(id_)

    async def update_musician(self, update_musician_dto: UpdateMusicianDTO) -> MusicianDTO:
        await UpdateMusician(self.uow)(update_musician_dto)
        return await GetMusicianById(self.uow)(update_musician_dto.id)

    async def delete_musician(self, id_: int) -> None:
        await DeleteMusician(self.uow)(id_)