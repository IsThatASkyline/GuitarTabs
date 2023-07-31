from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.infrastructure.db.uow import UnitOfWork


class DataBaseProvider:
    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        self.pool = pool

    async def provide_db(self):
        async with self.pool() as session:
            yield UnitOfWork(session)


def uow_provider():
    pass
