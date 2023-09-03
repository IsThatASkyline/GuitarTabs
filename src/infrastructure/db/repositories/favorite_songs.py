from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.application.guitarapp.dto import SongDTO, FavoriteSongDTO
from src.infrastructure.db.models import Song, User
from src.infrastructure.db.models.secondaries import UserFavorite
from src.infrastructure.db.repositories.base import BaseRepository


class FavoriteRepository(BaseRepository[UserFavorite]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(UserFavorite, session)

    async def create_obj(self, fav_dto: FavoriteSongDTO) -> None:
        query = select(User.id).where(User.telegram_id == fav_dto.user_id)
        user_id = (await self._session.execute(query)).scalar_one_or_none()

        fav = UserFavorite(
            song_id=fav_dto.song_id,
            user_id=user_id,
        )
        self.session.add(fav)

    async def get_all(self, user_id: int) -> list[SongDTO]:
        subquery = (select(User.id).where(User.telegram_id == user_id).scalar_subquery())
        query = select(Song).join(UserFavorite).where(UserFavorite.user_id == subquery).options(joinedload(Song.band))
        songs = (await self._session.execute(query)).scalars().all()
        return [song.to_dto() for song in songs]

    async def delete_obj(self, fav_dto: FavoriteSongDTO):
        subquery = (select(User.id).where(User.telegram_id == fav_dto.user_id).scalar_subquery())
        query = delete(UserFavorite).where(UserFavorite.user_id == subquery,
                                           UserFavorite.song_id == fav_dto.song_id)
        await self.session.execute(query)
