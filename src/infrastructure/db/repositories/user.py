from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.guitarapp.dto import CreateUserDTO, SongDTO
from src.infrastructure.db.models import User, Song, UserFavorite
from src.infrastructure.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(User, session)

    async def create_user(self, user_dto: CreateUserDTO) -> User:
        user = User(
            username=user_dto.username,
            email=user_dto.email,
            password=user_dto.password,
        )
        self.session.add(user)
        return user

    async def get_user_by_id(self, id_: int) -> User:
        return await super().get_by_id(id_)

    async def get_all_users(self) -> list[User]:
        return await super().get_all()

    async def update_user(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def delete_user(self, id_: int):
        await super().delete_obj(id_)
