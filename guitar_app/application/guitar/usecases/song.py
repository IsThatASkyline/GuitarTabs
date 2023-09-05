from guitar_app.application.common.usecases.base import BaseUseCase
from guitar_app.application.guitar.dto import FullSongDTO, CreateSongDTO, SongDTO, UpdateSongDTO, FavoriteSongDTO, \
    FindSongDTO, \
    ModulateSongDTO
from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.application.guitar.exceptions import SongNotExists, CreateSongException
from guitar_app.application.guitar.domain.services.modulation import get_modulate_verses


class SongUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)


class GetSongById(SongUseCase):
    async def __call__(self, id_: int) -> FullSongDTO:
        if song := await self.uow.app_holder.song_repo.get(id_):
            return song
        raise SongNotExists


class CreateSong(SongUseCase):
    async def __call__(self, song_dto: CreateSongDTO) -> int:
        if await self.uow.app_holder.band_repo.get(song_dto.band_id):
            try:
                return await self.uow.app_holder.song_repo.add(song_dto)
            except Exception as ex:
                print(ex)
        raise CreateSongException


class GetSongs(SongUseCase):
    async def __call__(self) -> list[SongDTO]:
        return await self.uow.app_holder.song_repo.list()


class GetFavoriteSongsByUser(SongUseCase):
    async def __call__(self, user_id: int) -> list[SongDTO]:
        return await self.uow.app_holder.favorites_repo.list(user_id)


class GetSongsByGroup(SongUseCase):
    async def __call__(self, band_id: int) -> list[SongDTO]:
        return await self.uow.app_holder.song_repo.get_songs_by_band(band_id)


class UpdateSong(SongUseCase):
    async def __call__(self, song_update_dto: UpdateSongDTO) -> None:
        if await self.uow.app_holder.song_repo.get(song_update_dto.id):
            await self.uow.app_holder.song_repo.update(
                song_update_dto.id,
                **song_update_dto.dict(exclude_none=True, exclude=set("id")),
            )
            return
        raise SongNotExists


class AddSongToFavorite(SongUseCase):
    async def __call__(self, song_dto: FavoriteSongDTO) -> bool:
        if song := await self.uow.app_holder.song_repo.get(song_dto.song_id):
            song = SongDTO(**song.dict())
            if song not in await self.uow.app_holder.favorites_repo.list(song_dto.user_id):
                return await self.uow.app_holder.favorites_repo.add(song_dto)
        raise SongNotExists


class RemoveSongFromFavorite(SongUseCase):
    async def __call__(self, song_dto: FavoriteSongDTO) -> bool:
        if song := await self.uow.app_holder.song_repo.get(song_dto.song_id):
            song = SongDTO(**song.dict())
            if song in await self.uow.app_holder.favorites_repo.list(song_dto.user_id):
                return await self.uow.app_holder.favorites_repo.delete(song_dto)
        raise SongNotExists


class FindSong(SongUseCase):
    async def __call__(self, song_dto: FindSongDTO) -> list[SongDTO] | None:
        if songs := await self.uow.app_holder.song_repo.find_song(song_dto):
            return songs
        return None


class GetModulatedSong(SongUseCase):
    async def __call__(self, song_modulate_dto: ModulateSongDTO) -> FullSongDTO:
        if song := await self.uow.app_holder.song_repo.get(song_modulate_dto.id):
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
        if await self.uow.app_holder.song_repo.get(id_):
            await self.uow.app_holder.song_repo.delete(id_)
            return
        raise SongNotExists
