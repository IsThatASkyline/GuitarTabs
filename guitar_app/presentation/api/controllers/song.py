from fastapi import APIRouter, Response, status
from fastapi.params import Depends

from guitar_app.application.guitar.dto import (
    BaseTabDTO,
    BaseVerseDTO,
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
    UserDTO,
)
from guitar_app.application.guitar.exceptions import CreateSongException, SongNotExists
from guitar_app.application.guitar.services import SongServices
from guitar_app.presentation.api.controllers.requests import (
    AddFavoriteSongRequest,
    CreateSongRequest,
    CreateTabRequest,
    FindSongRequest,
    ModulateSongRequest,
    RemoveFavoriteSongRequest,
    UpdateSongRequest,
)
from guitar_app.presentation.api.controllers.responses import (
    SongDeleteResponse,
    TabsDeleteResponse,
)
from guitar_app.presentation.api.controllers.responses.exceptions import (
    NotFoundSongError,
    SongIntegrityError,
)
from guitar_app.presentation.api.di.providers.services import get_song_services

router = APIRouter(prefix="/song", tags=["song"])


@router.post("/create-song")
async def create_song(
    song: CreateSongRequest,
    response: Response,
    song_services: SongServices = Depends(get_song_services),
) -> FullSongDTO | SongIntegrityError:
    try:
        response.status_code = status.HTTP_201_CREATED
        return await song_services.create_song(
            CreateSongDTO(
                title=song.title,
                band_id=song.band_id,
                description=song.description,
                verses=[
                    BaseVerseDTO(title=v.title, lyrics=v.lyrics, chords=v.chords)
                    for v in song.verses
                ]
                if song.verses
                else None,
            )
        )
    except CreateSongException:
        return SongIntegrityError()


@router.get("/get-all-songs")
async def get_all_songs(
    song_services: SongServices = Depends(get_song_services),
) -> list[SongDTO]:
    return await song_services.get_all_songs()


@router.get("/get-song/{song_id}")
async def get_song_by_id(
    song_id: int,
    response: Response,
    song_services: SongServices = Depends(get_song_services),
) -> FullSongDTO | NotFoundSongError:
    try:
        return await song_services.get_song_by_id(
            GetSongDTO(
                song_id=song_id,
            )
        )
    except SongNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundSongError()


@router.get("/get-user-favorite-songs/{user_id}")
async def get_favorite_songs(
    user_id: int, song_services: SongServices = Depends(get_song_services)
) -> list[SongDTO]:
    return await song_services.get_favorite_songs_by_user(UserDTO(telegram_id=user_id))


@router.patch("/update-song/{song_id}")
async def update_song(
    song_id: int,
    song: UpdateSongRequest,
    response: Response,
    song_services: SongServices = Depends(get_song_services),
) -> FullSongDTO | NotFoundSongError:
    try:
        return await song_services.update_song(UpdateSongDTO(id=song_id, **song.dict()))
    except SongNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundSongError()


@router.delete("/delete-song/{song_id}")
async def delete_song(
    song_id: int,
    response: Response,
    song_services: SongServices = Depends(get_song_services),
) -> SongDeleteResponse | NotFoundSongError:
    try:
        await song_services.delete_song(song_id)
        response.status_code = status.HTTP_204_NO_CONTENT
        return SongDeleteResponse()
    except SongNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundSongError()


@router.delete("/delete-tabs/{song_id}")
async def delete_tabs(
    song_id: int,
    response: Response,
    song_services: SongServices = Depends(get_song_services),
) -> TabsDeleteResponse | NotFoundSongError:
    try:
        await song_services.delete_tabs_in_song(song_id)
        response.status_code = status.HTTP_204_NO_CONTENT
        return TabsDeleteResponse()
    except SongNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundSongError()


@router.post("/modulate-song/{song_id}")
async def modulate_song(
    song_id: int,
    response: Response,
    value: ModulateSongRequest,
    song_services: SongServices = Depends(get_song_services),
) -> FullSongDTO | NotFoundSongError:
    try:
        return await song_services.modulate_song(ModulateSongDTO(id=song_id, **value.dict()))
    except SongNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundSongError()


@router.post("/add-song-to-favorite/{song_id}")
async def add_song_to_favorite(
    song_id: int,
    response: Response,
    user_id: AddFavoriteSongRequest,
    song_services: SongServices = Depends(get_song_services),
):
    try:
        await song_services.add_song_to_favorite(FavoriteSongDTO(song_id=song_id, **user_id.dict()))
        return {"detail": "Песня добавлена в избранное"}
    except SongNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundSongError()


@router.post("/remove-song-from-favorite/{song_id}")
async def remove_song_from_favorite(
    song_id: int,
    response: Response,
    user_id: RemoveFavoriteSongRequest,
    song_services: SongServices = Depends(get_song_services),
):
    try:
        await song_services.remove_song_from_favorite(
            FavoriteSongDTO(song_id=song_id, **user_id.dict())
        )
        return {"detail": "Песня убрана из избранного"}
    except SongNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundSongError()


@router.post("/find-song")
async def find_song(
    song: FindSongRequest,
    song_services: SongServices = Depends(get_song_services),
) -> list[SongDTO] | None:
    return await song_services.find_song(FindSongDTO(**song.dict()))


@router.post("/create-tabs/{song_id}")
async def create_tabs(
    song_id: int,
    tabs: list[CreateTabRequest],
    song_services: SongServices = Depends(get_song_services),
) -> list[TabDTO]:
    return await song_services.create_tabs(
        CreateTabDTO(
            song_id=song_id,
            tabs=[
                BaseTabDTO(
                    title=tab.title,
                    image_url=tab.image_url,
                )
                for tab in tabs
                if tabs
            ],
        )
    )
