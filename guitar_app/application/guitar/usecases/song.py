from guitar_app.application.common.usecases.base import BaseUseCase
from guitar_app.application.guitar.domain.services.modulation import (
    get_modulated_verses,
)
from guitar_app.application.guitar.dto import (
    CreateSongDTO,
    CreateTabDTO,
    FavoriteSongDTO,
    FindSongDTO,
    FullSongDTO,
    GetSongDTO,
    ModulateSongDTO,
    SongDTO,
    TabDTO,
    UpdateSongDTO,
)
from guitar_app.application.guitar.exceptions import CreateSongException, SongNotExists
from guitar_app.infrastructure.db.uow import UnitOfWork


class SongUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)


class GetSongById(SongUseCase):
    async def __call__(self, id_: int) -> FullSongDTO:
        if song := await self.uow.app_holder.song_repo.get_song(id_):
            return song
        raise SongNotExists


class GetTabById(SongUseCase):
    async def __call__(self, id_: int) -> TabDTO:
        if tab := await self.uow.app_holder.tab_repo.get_tab(id_):
            return tab
        raise Exception


class CreateSong(SongUseCase):
    async def __call__(self, song_dto: CreateSongDTO) -> int:
        if await self.uow.app_holder.band_repo.get_band(song_dto.band_id):
            return await self.uow.app_holder.song_repo.add_song(song_dto)
        raise CreateSongException


class CreateTabs(SongUseCase):
    async def __call__(self, tabs_dto: CreateTabDTO) -> int:
        if await self.uow.app_holder.song_repo.get_song(tabs_dto.song_id):
            return await self.uow.app_holder.tab_repo.add_tab(tabs_dto)
        raise Exception


class GetSongs(SongUseCase):
    async def __call__(self) -> list[SongDTO]:
        return await self.uow.app_holder.song_repo.list_songs()


class GetFavoriteSongsByUser(SongUseCase):
    async def __call__(self, user_id: int) -> list[SongDTO]:
        return await self.uow.app_holder.favorites_repo.get_user_favorite_songs(user_id)


class GetSongsByGroup(SongUseCase):
    async def __call__(self, band_id: int) -> list[SongDTO]:
        return await self.uow.app_holder.song_repo.get_songs_by_band(band_id)


class UpdateSong(SongUseCase):
    async def __call__(self, song_update_dto: UpdateSongDTO) -> None:
        if await self.uow.app_holder.song_repo.get_song(song_update_dto.id):
            await self.uow.app_holder.song_repo.update_song(song_update_dto)
            return
        raise SongNotExists


class AddSongToFavorite(SongUseCase):
    async def __call__(self, song_dto: FavoriteSongDTO) -> None:
        if song := await self.uow.app_holder.song_repo.get_song(song_dto.song_id):
            if (
                song.compress()
                not in await self.uow.app_holder.favorites_repo.get_user_favorite_songs(
                    song_dto.user_id
                )
            ):
                return await self.uow.app_holder.favorites_repo.add_favorite_song(song_dto)
        raise SongNotExists


class RemoveSongFromFavorite(SongUseCase):
    async def __call__(self, song_dto: FavoriteSongDTO) -> None:
        if song := await self.uow.app_holder.song_repo.get_song(song_dto.song_id):
            if song.compress() in await self.uow.app_holder.favorites_repo.get_user_favorite_songs(
                song_dto.user_id
            ):
                return await self.uow.app_holder.favorites_repo.delete_favorite_song(song_dto)
        raise SongNotExists


class FindSong(SongUseCase):
    async def __call__(self, song_dto: FindSongDTO) -> list[SongDTO] | None:
        if songs := await self.uow.app_holder.song_repo.find_song_by_title(song_dto):
            return songs
        return None


class GetTabsForSong(SongUseCase):
    async def __call__(self, id_: int) -> list[TabDTO] | None:
        if tabs := await self.uow.app_holder.song_repo.get_tabs_for_song(id_):
            return tabs
        raise SongNotExists


class GetModulatedSong(SongUseCase):
    async def __call__(self, song_modulate_dto: ModulateSongDTO) -> FullSongDTO:
        if song := await self.uow.app_holder.song_repo.get_song(song_modulate_dto.id):
            modulate_verses = get_modulated_verses(song.verses, song_modulate_dto.value)
            return FullSongDTO(
                id=song.id,
                title=song.title,
                band=song.band,
                verses=modulate_verses,
                hits_count=song.hits_count,
            )
        raise SongNotExists


class DeleteSong(SongUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.song_repo.get_song(id_):
            return await self.uow.app_holder.song_repo.delete_song(id_)
        raise SongNotExists


class DeleteTabs(SongUseCase):
    async def __call__(self, id_: int) -> None:
        if (await self.uow.app_holder.song_repo.get_song(id_)).tabs:
            return await self.uow.app_holder.tab_repo.delete_all_tabs_in_song(id_)
        raise Exception


class HitSong(SongUseCase):
    async def __call__(self, hit_dto: GetSongDTO) -> None:
        if hit_dto.user_id:
            if hit := await self.uow.app_holder.hit_counter_repo.get_hit(hit_dto):
                if not hit.can_be_hit:
                    return
                else:
                    await self.uow.app_holder.hit_counter_repo.delete_hit(hit.id)
            await self.uow.app_holder.hit_counter_repo.add_hit(hit_dto)
