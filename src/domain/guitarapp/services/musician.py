from src.domain.guitarapp.dto import CreateMusicianDTO, MusicianDTO, UpdateMusicianDTO
from src.domain.guitarapp.usecases import CreateMusician, GetMusicians, GetMusicianById, UpdateMusician, DeleteMusician
from src.infrastructure.db.uow import UnitOfWork


class MusicianServices:
    def __init__(self, uow: UnitOfWork) -> None:
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
