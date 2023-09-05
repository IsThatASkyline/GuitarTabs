from guitar_app.application.guitar.dto import CreateMusicianDTO, MusicianDTO, UpdateMusicianDTO
from guitar_app.application.guitar.usecases import CreateMusician, GetMusicians, GetMusicianById, UpdateMusician, DeleteMusician
from guitar_app.infrastructure.db.uow import AbstractUnitOfWork


class MusicianServices:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def create_musician(self, musician_dto: CreateMusicianDTO) -> MusicianDTO:
        async with self.uow:
            musician = await CreateMusician(self.uow)(musician_dto)
            await self.uow.commit()
            return musician

    async def get_all_musicians(self) -> list[MusicianDTO]:
        return await GetMusicians(self.uow)()

    async def get_musician_by_id(self, id_: int) -> MusicianDTO:
        return await GetMusicianById(self.uow)(id_)

    async def update_musician(self, update_musician_dto: UpdateMusicianDTO) -> MusicianDTO:
        async with self.uow:
            await UpdateMusician(self.uow)(update_musician_dto)
            await self.uow.commit()
            return await GetMusicianById(self.uow)(update_musician_dto.id)

    async def delete_musician(self, id_: int) -> None:
        async with self.uow:
            await DeleteMusician(self.uow)(id_)
            await self.uow.commit()
