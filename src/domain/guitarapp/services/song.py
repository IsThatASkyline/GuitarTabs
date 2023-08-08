from sqlalchemy.exc import IntegrityError

from src.application.services.modulation import get_modulate_verses
from src.domain.guitarapp.dto.song import CreateSongDTO, SongDTO, UpdateSongDTO, FullSongDTO, ModulateSongDTO
from src.domain.guitarapp.exceptions import SongNotExists, CreateSongException
from src.domain.guitarapp.usecases import SongUseCase
from src.infrastructure.db.uow import UnitOfWork


class GetSongById(SongUseCase):
    async def __call__(self, id_: int) -> FullSongDTO:
        try:
            song = await self.uow.app_holder.song_repo.get_by_id(id_)
            return song
        except Exception:
            raise SongNotExists


class CreateSong(SongUseCase):
    async def __call__(self, song_dto: CreateSongDTO) -> SongDTO:
        if await self.uow.app_holder.band_repo.get_by_id(song_dto.band_id):
            song = await self.uow.app_holder.song_repo.create_obj(song_dto)
            await self.uow.commit()
            return song
        raise CreateSongException


class GetSongs(SongUseCase):
    async def __call__(self) -> list[SongDTO]:
        songs = await self.uow.app_holder.song_repo.get_all()
        return songs


class UpdateSong(SongUseCase):
    async def __call__(self, song_update_dto: UpdateSongDTO) -> None:
        await self.uow.app_holder.song_repo.update_obj(
            song_update_dto.id,
            **song_update_dto.dict(exclude_none=True, exclude=set("id")),
        )
        await self.uow.commit()


class ModulateSong(SongUseCase):
    async def __call__(self, song_modulate_dto: ModulateSongDTO) -> FullSongDTO:
        try:
            song = await self.uow.app_holder.song_repo.get_by_id(song_modulate_dto.id)
            modulate_verses = get_modulate_verses(song.verses, song_modulate_dto.value)
            modulate_song = FullSongDTO(
                id=song.id,
                title=song.title,
                band_id=song.band_id,
                verses=modulate_verses
            )
            return modulate_song
        except Exception as ex:
            print(ex)


class DeleteSong(SongUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.song_repo.get_by_id(id_):
            await self.uow.app_holder.song_repo.delete_obj(id_)
            await self.uow.commit()
            return
        raise SongNotExists


class SongServices:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_song(self, user_dto: CreateSongDTO) -> SongDTO:
        return await CreateSong(self.uow)(user_dto)

    async def get_all_songs(self) -> list[SongDTO]:
        return await GetSongs(self.uow)()

    async def get_song_by_id(self, id_: int) -> FullSongDTO:
        return await GetSongById(self.uow)(id_)

    async def update_song(self, update_song_dto: UpdateSongDTO) -> FullSongDTO:
        await UpdateSong(self.uow)(update_song_dto)
        return await GetSongById(self.uow)(update_song_dto.id)

    async def delete_song(self, id_: int) -> None:
        await DeleteSong(self.uow)(id_)

    async def modulate_song(self, modulate_song_dto: ModulateSongDTO) -> FullSongDTO:
        return await ModulateSong(self.uow)(modulate_song_dto)
