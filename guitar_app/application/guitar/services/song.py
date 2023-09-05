from guitar_app.application.guitar.dto import UserDTO
from guitar_app.application.guitar.dto.song import CreateSongDTO, SongDTO, UpdateSongDTO, FullSongDTO, ModulateSongDTO, \
    FavoriteSongDTO, FindSongDTO
from guitar_app.application.guitar.usecases import CreateSong, GetSongs, GetSongById, UpdateSong, DeleteSong, \
    GetModulatedSong, FindSong, GetFavoriteSongsByUser, AddSongToFavorite, RemoveSongFromFavorite, \
    GetSongsByGroup
from guitar_app.infrastructure.db.uow import AbstractUnitOfWork


class SongServices:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def create_song(self, song_dto: CreateSongDTO) -> SongDTO:
        async with self.uow:
            song_id = await CreateSong(self.uow)(song_dto)
            await self.uow.commit()
            return await GetSongById(self.uow)(song_id)

    async def get_all_songs(self) -> list[SongDTO]:
        return await GetSongs(self.uow)()

    async def get_song_by_id(self, id_: int) -> FullSongDTO:
        return await GetSongById(self.uow)(id_)

    async def get_favorite_songs_by_user(self, user_dto: UserDTO) -> list[SongDTO]:
        return await GetFavoriteSongsByUser(self.uow)(user_dto.telegram_id)

    async def get_songs_by_band(self, band_id: int) -> list[SongDTO]:
        return await GetSongsByGroup(self.uow)(band_id)

    async def update_song(self, update_song_dto: UpdateSongDTO) -> FullSongDTO:
        async with self.uow:
            await UpdateSong(self.uow)(update_song_dto)
            await self.uow.commit()
            return await GetSongById(self.uow)(update_song_dto.id)

    async def delete_song(self, id_: int) -> None:
        async with self.uow:
            await DeleteSong(self.uow)(id_)
            await self.uow.commit()

    async def modulate_song(self, modulate_song_dto: ModulateSongDTO) -> FullSongDTO:
        return await GetModulatedSong(self.uow)(modulate_song_dto)

    async def add_song_to_favorite(self, song_dto: FavoriteSongDTO):
        async with self.uow:
            await AddSongToFavorite(self.uow)(song_dto)
            await self.uow.commit()

    async def remove_song_from_favorite(self, song_dto: FavoriteSongDTO):
        async with self.uow:
            await RemoveSongFromFavorite(self.uow)(song_dto)
            await self.uow.commit()

    async def find_song(self, song_dto: FindSongDTO) -> list[SongDTO]:
        return await FindSong(self.uow)(song_dto)
