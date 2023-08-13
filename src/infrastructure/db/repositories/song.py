from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

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
        song = await super().get_by_id(id_)

        query = select(Verse).where(Verse.song_id == id_)
        verses = (await self.session.execute(query)).scalars().all()
        return song.to_full_dto(verses=verses) if song else None

    async def get_all(self) -> list[SongDTO]:
        songs = await super().get_all()
        return [song.to_dto() for song in songs] if songs else None

    async def update_obj(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)

    async def add_song_to_favorite(self, song_dto: FavoriteSongDTO) -> None:
        fav = UserFavorite(
            song_id=song_dto.id,
            user_id=song_dto.user_id,
        )
        self.session.add(fav)
        await self.session.flush()

    async def remove_song_from_favorite(self, song_dto: FavoriteSongDTO) -> None:
        query = delete(UserFavorite).where(UserFavorite.song_id == song_dto.id)
        await self.session.execute(query)

    async def get_favorite_songs_by_user(self, id_: int) -> list[SongDTO]:
        query = select(Song).join(UserFavorite).where(UserFavorite.user_id == id_)
        songs = (await self._session.execute(query)).scalars().all()
        return [song.to_dto() for song in songs]

    async def delete_obj(self, id_: int):
        await super().delete_obj(id_)
