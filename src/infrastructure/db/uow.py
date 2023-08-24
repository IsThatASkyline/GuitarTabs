from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.repositories import (UserRepository, MusicianRepository, SongRepository,
                                                BandRepository, FavoriteRepository, BandMembersRepository,
                                                FindSongRepository)


class SqlAlchemyUOW:
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


class AppHolder:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repo = UserRepository(session)
        self.musician_repo = MusicianRepository(session)
        self.band_repo = BandRepository(session)
        self.song_repo = SongRepository(session)
        self.find_song_repo = FindSongRepository(session)
        self.favorites_repo = FavoriteRepository(session)
        self.band_members_repo = BandMembersRepository(session)


class UnitOfWork(SqlAlchemyUOW):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

        self.app_holder = AppHolder(session)
