from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.guitarapp.dto import CreateSongDTO, SongDTO, FullSongDTO, FavoriteSongDTO
from src.infrastructure.db.models.secondaries import UserFavorite
from src.infrastructure.db.repositories.base import BaseRepository


class FavoriteRepository(BaseRepository[UserFavorite]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(UserFavorite, session)

    async def create_obj(self, fav_dto: FavoriteSongDTO) -> None:
        fav = UserFavorite(
            song_id=fav_dto.song_id,
            user_id=fav_dto.user_id,
        )
        self.session.add(fav)
        await self.session.flush()

    async def delete_obj(self, fav_dto: FavoriteSongDTO):
        query = delete(UserFavorite).where(UserFavorite.user_id == fav_dto.user_id,
                                           UserFavorite.song_id == fav_dto.song_id)
        await self.session.execute(query)