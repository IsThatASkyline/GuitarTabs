from src.application.guitarapp.dto.song import CreateSongDTO, SongDTO, UpdateSongDTO, FullSongDTO, ModulateSongDTO, \
    FavoriteSongDTO, FindSongDTO
from src.application.guitarapp.usecases import CreateSong, GetSongs, GetSongById, UpdateSong, DeleteSong, GetModulatedSong, \
    SongToFavorite, FindSong
from src.infrastructure.db.uow import UnitOfWork


class SongServices:
    def __init__(self, uow: UnitOfWork) -> None:
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

    async def song_to_favorite(self,  song_dto: FavoriteSongDTO) -> bool:
        async with self.uow:
            is_added = await SongToFavorite(self.uow)(song_dto)
            await self.uow.commit()
            return is_added

    async def find_song(self, song_dto: FindSongDTO) -> list[SongDTO]:
        return await FindSong(self.uow)(song_dto)