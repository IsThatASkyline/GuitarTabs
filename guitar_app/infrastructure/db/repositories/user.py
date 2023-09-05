from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from guitar_app.application.guitar.dto import CreateUserDTO, UserDTO
from guitar_app.infrastructure.db.models import User
from guitar_app.infrastructure.db.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(User, session)

    async def add(self, user_dto: CreateUserDTO) -> UserDTO:
        user = User(
            telegram_id=user_dto.telegram_id,
            username=user_dto.username
        )
        self.session.add(user)
        return user.to_dto()

    async def get(self, id_: int) -> UserDTO | None:
        query = select(User).where(User.telegram_id == id_)
        user = (await self._session.execute(query)).scalar_one_or_none()
        return user.to_dto() if user else None

    async def list(self) -> list[UserDTO]:
        query = select(User)
        users = (await self._session.execute(query)).scalars()
        return [user.to_dto() for user in users]

    async def update(self, id_: int, **kwargs) -> None:
        await super().update(id_, **kwargs)

    async def delete(self, id_: int):
        await super().delete(id_)
