from src.application.common.usecases.base import BaseUseCase
from src.application.guitarapp.dto import FullSongDTO, CreateSongDTO, SongDTO, UpdateSongDTO, FavoriteSongDTO, FindSongDTO, \
    ModulateSongDTO
from src.infrastructure.db.uow import UnitOfWork
from src.application.guitarapp.exceptions import SongNotExists, CreateSongException
from src.application.guitarapp.utils.modulation import get_modulate_verses


class SongUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)


class GetSongById(SongUseCase):
    async def __call__(self, id_: int) -> FullSongDTO:
        if song := await self.uow.app_holder.song_repo.get_by_id(id_):
            return song
        raise SongNotExists


class CreateSong(SongUseCase):
    async def __call__(self, song_dto: CreateSongDTO) -> int:
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


class FindSong(SongUseCase):
    async def __call__(self, song_dto: FindSongDTO) -> list[SongDTO] | None:
        if songs := await self.uow.app_holder.song_repo.find_song(song_dto):
            return songs
        return None


class GetModulatedSong(SongUseCase):
    async def __call__(self, song_modulate_dto: ModulateSongDTO) -> FullSongDTO:
        if song := await self.uow.app_holder.song_repo.get_by_id(song_modulate_dto.id):
            modulate_verses = get_modulate_verses(song.verses, song_modulate_dto.value)
            return FullSongDTO(
                id=song.id,
                title=song.title,
                band=song.band,
                verses=modulate_verses
            )
        raise SongNotExists


class DeleteSong(SongUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.song_repo.get_by_id(id_):
            await self.uow.app_holder.song_repo.delete_obj(id_)
            return
        raise SongNotExists

