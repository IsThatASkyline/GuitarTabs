from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from guitar_app.application.guitar.dto import CreateSongDTO, SongDTO, FullSongDTO, FindSongDTO
from guitar_app.infrastructure.db.models import Song, Verse
from guitar_app.infrastructure.db.repositories.base import BaseRepository


class SongRepository(BaseRepository[Song]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Song, session)

    async def create_obj(self, song_dto: CreateSongDTO) -> int:
        song = Song(
            title=song_dto.title,
            band_id=song_dto.band_id,
        )
        self.session.add(song)
        await self.session.flush()

        if song_dto.verses:
            for v in song_dto.verses:
                self.session.add(
                    Verse(
                        title=v.title,
                        lyrics=v.lyrics,
                        chords=v.chords,
                        song_id=song.id,
                    )
                )

        return song.id

    async def get_by_id(self, id_: int) -> FullSongDTO:
        query = select(Song).options(joinedload(Song.verses), joinedload(Song.band)).where(Song.id == id_)
        song = (await self.session.execute(query)).unique().scalar_one_or_none()
        return song.to_full_dto() if song else None

    async def get_all(self) -> list[SongDTO]:
        query = select(Song).options(joinedload(Song.band))
        songs = (await self.session.execute(query)).scalars().all()
        return [song.to_dto() for song in songs] if songs else None

    async def get_songs_by_band(self, band_id) -> list[SongDTO]:
        query = select(Song).options(joinedload(Song.band)).where(Song.band_id == band_id)
        songs = (await self.session.execute(query)).scalars().all()
        return [song.to_dto() for song in songs] if songs else None

    async def find_song(self, criteria: FindSongDTO) -> list[SongDTO]:
        query = select(Song).options(joinedload(Song.band)).where(Song.title.ilike('%' + criteria.value + '%'))
        songs = (await self.session.execute(query, params=criteria.dict())).scalars().all()
        return [song.to_dto() for song in songs] if songs else None

    async def update_obj(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def delete_obj(self, id_: int):
        await super().delete_obj(id_)