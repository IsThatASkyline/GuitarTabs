from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.guitarapp.dto import CreateSongDTO, SongDTO, FullSongDTO
from src.infrastructure.db.models import Song
from src.infrastructure.db.repositories.base import BaseRepository


class SongRepository(BaseRepository[Song]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Song, session)

    async def create_obj(self, song_dto: CreateSongDTO) -> SongDTO:
        song = Song(
            title=song_dto.title,
            lyrics=song_dto.lyrics,
            band_id=song_dto.band_id,
        )
        self.session.add(song)
        await self.session.flush()
        return song.to_dto()

    async def get_by_id(self, id_: int) -> FullSongDTO:
        song = await super().get_by_id(id_)
        return song.to_full_dto() if song else None

    async def get_all(self) -> list[SongDTO]:
        songs = await super().get_all()
        return [song.to_dto() for song in songs] if songs else None

    async def update_obj(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def delete_obj(self, id_: int):
        await super().delete_obj(id_)
