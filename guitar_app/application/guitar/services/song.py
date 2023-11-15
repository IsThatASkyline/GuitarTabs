from guitar_app.application.guitar.dto import UserDTO, TabDTO, CreateTabDTO
from guitar_app.application.guitar.dto.song import (
    CreateSongDTO,
    FavoriteSongDTO,
    FindSongDTO,
    FullSongDTO,
    GetSongDTO,
    ModulateSongDTO,
    SongDTO,
    UpdateSongDTO,
)
from guitar_app.application.guitar.usecases import (
    AddSongToFavorite,
    CreateSong,
    DeleteSong,
    FindSong,
    GetFavoriteSongsByUser,
    GetModulatedSong,
    GetSongById,
    GetSongs,
    GetSongsByGroup,
    HitSong,
    RemoveSongFromFavorite,
    UpdateSong,
    GetTabsForSong,
    DeleteTabs,
)
from guitar_app.application.guitar.usecases.song import CreateTabs, GetTabById
from guitar_app.infrastructure.db.uow import UnitOfWork


class SongServices:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_song(self, song_dto: CreateSongDTO) -> FullSongDTO:
        async with self.uow:
            song_id = await CreateSong(self.uow)(song_dto)
            await self.uow.commit()
            return await GetSongById(self.uow)(song_id)

    async def get_all_songs(self) -> list[SongDTO]:
        return await GetSongs(self.uow)()

    async def get_song_by_id(self, get_song_dto: GetSongDTO) -> FullSongDTO:
        async with self.uow:
            await HitSong(self.uow)(get_song_dto)
            await self.uow.commit()
            return await GetSongById(self.uow)(get_song_dto.song_id)

    async def create_tabs(self, tabs_dto: CreateTabDTO) -> list[TabDTO]:
        async with self.uow:
            await CreateTabs(self.uow)(tabs_dto)
            await self.uow.commit()
            return await GetTabsForSong(self.uow)(tabs_dto.song_id)

    async def get_tabs_for_song(self, id_: int) -> list[TabDTO]:
        return await GetTabsForSong(self.uow)(id_)

    async def get_tab(self, id_: int) -> TabDTO:
        return await GetTabById(self.uow)(id_)

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

    async def delete_tabs_in_song(self, id_: int) -> None:
        async with self.uow:
            await DeleteTabs(self.uow)(id_)
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
