from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.guitarapp.dto import CreateUserDTO, UserDTO
from src.infrastructure.db.models import User
from src.infrastructure.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(User, session)

    async def create_user(self, user_dto: CreateUserDTO) -> UserDTO:
        user = User(
            telegram_id=user_dto.telegram_id,
        )
        self.session.add(user)
        return user.to_dto()

    async def get_user_by_id(self, id_: int) -> UserDTO:
        query = select(User).where(User.telegram_id == id_)
        user: User = (await self._session.execute(query)).scalar_one_or_none()
        return user.to_dto()

    async def get_all_users(self) -> list[UserDTO]:
        query = select(User)
        users = (await self._session.execute(query)).scalars()
        return [user.to_dto() for user in users]

    async def update_user(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def delete_user(self, id_: int):
        await super().delete_obj(id_)
