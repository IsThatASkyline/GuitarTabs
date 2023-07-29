from sqlalchemy.ext.asyncio import AsyncSession

from guitar_app.src.domain.guitarapp.dto import CreateMusicianDTO
from guitar_app.src.infrastructure.db.models import Musician
from guitar_app.src.infrastructure.db.repositories.base import BaseRepository


class MusucianRepository(BaseRepository[Musician]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Musician, session)

    async def create_user(self, musician_dto: CreateMusicianDTO) -> Musician:
        musician = Musician(
            name=musician_dto.musicianname,
            email=musician_dto.email,
            password=musician_dto.password,
        )
        self.session.add(musician)
        return musician

    async def get_musician_by_id(self, id_: int) -> Musician:
        return await super().get_by_id(id_)

    async def get_all_musicians(self) -> list[Musician]:
        return await super().get_all()

    async def update_musician(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def delete_musician(self, id_: int):
        await super().delete_obj(id_)
