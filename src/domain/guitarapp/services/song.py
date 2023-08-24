from src.domain.guitarapp.utils.modulation import get_modulate_verses
from src.domain.guitarapp.dto.song import CreateSongDTO, SongDTO, UpdateSongDTO, FullSongDTO, ModulateSongDTO, \
    FavoriteSongDTO
from src.domain.guitarapp.exceptions import SongNotExists, CreateSongException
from src.domain.guitarapp.usecases import SongUseCase
from src.infrastructure.db.uow import UnitOfWork


class GetSongById(SongUseCase):
    async def __call__(self, id_: int) -> FullSongDTO:
        if song := await self.uow.app_holder.song_repo.get_by_id(id_):
            return song
        raise SongNotExists


class CreateSong(SongUseCase):
    async def __call__(self, song_dto: CreateSongDTO) -> SongDTO:
        if await self.uow.app_holder.band_repo.get_by_id(song_dto.band_id):
            try:
                return await self.uow.app_holder.song_repo.create_obj(song_dto)
            except Exception as ex:
                print(ex)
        raise CreateSongException


class GetSongs(SongUseCase):
    async def __call__(self) -> list[SongDTO]:
        return await self.uow.app_holder.song_repo.get_all()


class UpdateSong(SongUseCase):
    async def __call__(self, song_update_dto: UpdateSongDTO) -> None:
        if await self.uow.app_holder.song_repo.get_by_id(song_update_dto.id):
            await self.uow.app_holder.song_repo.update_obj(
                song_update_dto.id,
                **song_update_dto.dict(exclude_none=True, exclude=set("id")),
            )
            return
        raise SongNotExists


class SongToFavorite(SongUseCase):
    async def __call__(self, song_dto: FavoriteSongDTO) -> bool:
        # if song already in favorites, delete song from favorites and return False
        # else add song to favorites and return True
        if song := await self.uow.app_holder.song_repo.get_by_id(song_dto.song_id):
            song = SongDTO(**song.dict())
            if song in await self.uow.app_holder.favorites_repo.get_all(song_dto.user_id):
                await self.uow.app_holder.favorites_repo.delete_obj(song_dto)
                return False
            else:
                await self.uow.app_holder.favorites_repo.create_obj(song_dto)
                return True
        raise SongNotExists


class GetModulatedSong(SongUseCase):
    async def __call__(self, song_modulate_dto: ModulateSongDTO) -> FullSongDTO:
        if song := await self.uow.app_holder.song_repo.get_by_id(song_modulate_dto.id):
            modulate_verses = get_modulate_verses(song.verses, song_modulate_dto.value)
            return FullSongDTO(
                id=song.id,
                title=song.title,
                band_id=song.band_id,
                verses=modulate_verses
            )
        raise SongNotExists


class DeleteSong(SongUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.song_repo.get_by_id(id_):
            await self.uow.app_holder.song_repo.delete_obj(id_)
            return
        raise SongNotExists


class SongServices:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_song(self, user_dto: CreateSongDTO) -> SongDTO:
        async with self.uow:
            song = await CreateSong(self.uow)(user_dto)
            await self.uow.commit()
            return song

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