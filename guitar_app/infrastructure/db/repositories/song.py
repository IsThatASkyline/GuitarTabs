from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from guitar_app.application.guitar.dto import (
    CreateSongDTO,
    FindSongDTO,
    FullSongDTO,
    SongDTO,
    TabDTO,
    UpdateSongDTO,
)
from guitar_app.infrastructure.db.models import Song, Tab, Verse
from guitar_app.infrastructure.db.repositories.base import BaseRepository


class SongRepository(BaseRepository[Song]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Song, session)

    async def add_song(self, song_dto: CreateSongDTO) -> int:
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

    async def get_song(self, id_: int) -> FullSongDTO:
        query = (
            select(Song)
            .options(joinedload(Song.verses), joinedload(Song.band), joinedload(Song.tabs))
            .where(Song.id == id_)
        )
        song = (await self.session.execute(query)).unique().scalar_one_or_none()
        return song.to_full_dto() if song else None

    async def get_tabs_for_song(self, id_: int) -> list[TabDTO]:
        query = select(Tab).where(Tab.song_id == id_)
        tabs = (await self.session.execute(query)).scalars().all()
        return [tab.to_dto() for tab in tabs] if tabs else None

    async def list_songs(self) -> list[SongDTO]:
        query = select(Song).options(joinedload(Song.band)).order_by(Song.title)
        songs = (await self.session.execute(query)).scalars().all()
        return [song.to_dto() for song in songs] if songs else None

    async def get_songs_by_band(self, band_id):
        query = (
            select(Song)
            .options(joinedload(Song.band))
            .where(Song.band_id == band_id)
            .order_by(Song.title)
        )
        songs = (await self.session.execute(query)).scalars().all()
        return [song.to_dto() for song in songs] if songs else None

    async def find_song_by_title(self, criteria: FindSongDTO):
        query = (
            select(Song)
            .options(joinedload(Song.band))
            .where(Song.title.ilike("%" + criteria.value + "%"))
            .order_by(Song.title)
        )
        songs = (await self.session.execute(query)).scalars().all()
        return [song.to_dto() for song in songs] if songs else None

    async def update_song(self, update_song_dto: UpdateSongDTO) -> None:
        await super().update(id_=update_song_dto.id, title=update_song_dto.title)

    async def delete_song(self, id_: int):
        await super().delete(id_)
