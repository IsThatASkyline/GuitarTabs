from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.guitarapp.dto import CreateSongDTO
from src.infrastructure.db.models import Song
from src.infrastructure.db.repositories.base import BaseRepository


class SongRepository(BaseRepository[Song]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Song, session)

    async def create_song(self, song_dto: CreateSongDTO) -> Song:
        song = Song(
            title=song_dto.title,
            lyrics=song_dto.lyrics,
            band_id=song_dto.band_id,
        )
        self.session.add(song)
        return song

    async def get_song_by_id(self, id_: int) -> Song:
        return await super().get_by_id(id_)

    async def get_all_songs(self) -> list[Song]:
        return await super().get_all()

    async def update_song(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def delete_song(self, id_: int):
        await super().delete_obj(id_)
