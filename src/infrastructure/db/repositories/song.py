from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.domain.guitarapp.dto import CreateSongDTO, SongDTO, FullSongDTO, FavoriteSongDTO
from src.infrastructure.db.models import Song, Verse
from src.infrastructure.db.models.secondaries import UserFavorite
from src.infrastructure.db.repositories.base import BaseRepository


class SongRepository(BaseRepository[Song]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Song, session)

    async def create_obj(self, song_dto: CreateSongDTO) -> SongDTO:
        song = Song(
            title=song_dto.title,
            band_id=song_dto.band_id,
        )
        self.session.add(song)
        await self.session.flush()

        if song_dto.verses:
            [self.session.add(Verse(
                title=v.title,
                lyrics=v.lyrics,
                chords=v.chords,
                song_id=song.id,
            )) for v in song_dto.verses]

        return song.to_dto()

    async def get_by_id(self, id_: int) -> FullSongDTO:
        query = select(Song).options(joinedload(Song.verses)).where(Song.id == id_)
        song = (await self.session.execute(query)).unique().scalar_one_or_none()
        return song.to_full_dto() if song else None

    async def get_all(self) -> list[SongDTO]:
        songs = await super().get_all()
        return [song.to_dto() for song in songs] if songs else None

    async def update_obj(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def delete_obj(self, id_: int):
        await super().delete_obj(id_)
