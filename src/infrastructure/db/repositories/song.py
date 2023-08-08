from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.guitarapp.dto import CreateSongDTO, SongDTO, FullSongDTO
from src.infrastructure.db.models import Song, Verse
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
        song = await super().get_by_id(id_)

        query = select(Verse).where(Verse.song_id == song.id)
        verses = (await self._session.execute(query)).scalars().all()
        return song.to_full_dto(verses=verses) if song else None

    async def get_all(self) -> list[SongDTO]:
        songs = await super().get_all()
        return [song.to_dto() for song in songs] if songs else None

    async def update_obj(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def delete_obj(self, id_: int):
        await super().delete_obj(id_)
