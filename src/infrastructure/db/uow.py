from sqlalchemy.ext.asyncio import AsyncSession

from guitar_app.src.infrastructure.db.repositories import UserRepository, MusucianRepository


class SqlAlchemyUOW:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class AppHolder:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repo = UserRepository(session)
        self.musician_repo = MusucianRepository(session)


class UnitOfWork(SqlAlchemyUOW):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

        self.app_holder = AppHolder(session)
