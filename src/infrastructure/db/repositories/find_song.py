from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.domain.guitarapp.dto import SongDTO, FindSongDTO
from src.infrastructure.db.models import Song
from src.infrastructure.db.repositories.base import BaseRepository


class FindSongRepository(BaseRepository[Song]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Song, session)

    async def get_all(self, criteria: FindSongDTO) -> list[SongDTO]:
        query = select(Song).options(joinedload(Song.band)).where(Song.title.ilike('%' + criteria.value + '%'))
        songs = (await self.session.execute(query, params=criteria.dict())).scalars().all()
        return [song.to_dto() for song in songs] if songs else None
