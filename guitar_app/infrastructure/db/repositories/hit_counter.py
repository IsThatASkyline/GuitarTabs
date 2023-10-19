from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from guitar_app.application.guitar.dto import GetSongDTO, HitDTO
from guitar_app.infrastructure.db.models import HitCounterBlacklist, Song, User
from guitar_app.infrastructure.db.repositories.base import BaseRepository


class HitCounterRepository(BaseRepository[HitCounterBlacklist]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(HitCounterBlacklist, session)

    async def add_hit(self, hit_dto: GetSongDTO):
        query = update(Song).values(hits_count=Song.hits_count + 1).where(Song.id == hit_dto.song_id)
        await self.session.execute(query)
        subquery = select(User.id).where(User.telegram_id == hit_dto.user_id).scalar_subquery()
        timeout = HitCounterBlacklist(
            song_id=hit_dto.song_id,
            user_id=subquery,
        )
        self.session.add(timeout)

    async def get_hit(self, hit_dto: GetSongDTO) -> HitDTO:
        subquery = select(User.id).where(User.telegram_id == hit_dto.user_id).scalar_subquery()
        query = select(HitCounterBlacklist).where(
            HitCounterBlacklist.user_id == subquery, HitCounterBlacklist.song_id == hit_dto.song_id
        )
        hit = (await self._session.execute(query)).unique().scalar_one_or_none()
        return hit.to_dto() if hit else None

    async def delete_hit(self, id_: int):
        await super().delete(id_)
