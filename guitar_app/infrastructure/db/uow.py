import abc

from sqlalchemy.ext.asyncio import AsyncSession

from guitar_app.infrastructure.db.repositories import (
    BandMembersRepository,
    BandRepository,
    FavoriteRepository,
    HitCounterRepository,
    MusicianRepository,
    SongRepository,
    UserRepository, TabRepository,
)


class AbstractUnitOfWork(abc.ABC):
    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUOW(AbstractUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class AbstractHolder:
    pass


class AppHolder(AbstractHolder):
    def __init__(self, session: AsyncSession) -> None:
        self.user_repo = UserRepository(session)
        self.musician_repo = MusicianRepository(session)
        self.band_repo = BandRepository(session)
        self.song_repo = SongRepository(session)
        self.tab_repo = TabRepository(session)
        self.favorites_repo = FavoriteRepository(session)
        self.band_members_repo = BandMembersRepository(session)
        self.hit_counter_repo = HitCounterRepository(session)


class UnitOfWork(SqlAlchemyUOW):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

        self.app_holder = AppHolder(session)
