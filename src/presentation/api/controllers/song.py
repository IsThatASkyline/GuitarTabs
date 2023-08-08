from fastapi import APIRouter, Response, status
from fastapi.params import Depends

from src.domain.guitarapp.dto import CreateSongDTO, SongDTO, UpdateSongDTO, FullSongDTO
from src.domain.guitarapp.exceptions import SongNotExists, CreateSongException
from src.domain.guitarapp.services import SongServices
from src.presentation.api.controllers.requests import (
    CreateSongRequest,
    UpdateSongRequest,
    ModulateSongRequest
)
from src.presentation.api.controllers.responses import SongDeleteResponse
from src.presentation.api.controllers.responses.exceptions import NotFoundSongError, SongIntegrityError
from src.presentation.api.di.providers.services import get_song_services

router = APIRouter(prefix="/song", tags=["song"])


@router.post("/create-song")
async def create_song(
    song: CreateSongRequest,
    response: Response,
    song_services: SongServices = Depends(get_song_services),
) -> SongDTO | SongIntegrityError:
    try:
        response.status_code = status.HTTP_201_CREATED
        return await song_services.create_song(CreateSongDTO(**song.dict()))
    except CreateSongException:
        return SongIntegrityError()

@router.get("/get-all-songs")
async def get_all_songs(
    song_services: SongServices = Depends(get_song_services),
) -> list[SongDTO]:
    return await song_services.get_all_songs()


@router.get("/get-song/{song_id}")
async def get_song_by_id(
    song_id: int, song_services: SongServices = Depends(get_song_services)
) -> FullSongDTO | NotFoundSongError:
    try:
        return await song_services.get_song_by_id(song_id)
    except SongNotExists:
        return NotFoundSongError()


@router.patch("/update-song/{song_id}")
async def update_song(
    song_id: int,
    song: UpdateSongRequest,
    song_services: SongServices = Depends(get_song_services),
) -> FullSongDTO:
    return await song_services.update_song(UpdateSongDTO(id=song_id, **song.dict()))


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


@router.delete("/modulate/{song_id}")
async def modulate_song(
    song_id: int,
    song: ModulateSongRequest,
    song_services: SongServices = Depends(get_song_services),
) -> FullSongDTO:
    return await song_services.update_song(UpdateSongDTO(id=song_id, **song.dict()))
