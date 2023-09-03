from fastapi import APIRouter, Response, status
from fastapi.params import Depends
from guitar_app.application.guitar.dto import CreateMusicianDTO, MusicianDTO, UpdateMusicianDTO
from guitar_app.application.guitar.exceptions import MusicianNotExists
from guitar_app.application.guitar.services import MusicianServices
from guitar_app.presentation.api.controllers.requests import (
    CreateMusicianRequest,
    UpdateMusicianRequest,
)
from guitar_app.presentation.api.controllers.responses import MusicianDeleteResponse
from guitar_app.presentation.api.controllers.responses.exceptions import NotFoundMusicianError
from guitar_app.presentation.api.di.providers.services import get_musician_services


router = APIRouter(prefix="/musician", tags=["musician"])


@router.post("/create-musician")
async def create_musician(
    musician: CreateMusicianRequest,
    response: Response,
    musician_services: MusicianServices = Depends(get_musician_services),
) -> MusicianDTO:
    response.status_code = status.HTTP_201_CREATED
    return await musician_services.create_musician(CreateMusicianDTO(**musician.dict()))


@router.get("/get-all-musicians")
async def get_all_musicians(
    musician_services: MusicianServices = Depends(get_musician_services),
) -> list[MusicianDTO]:
    return await musician_services.get_all_musicians()


@router.get("/get-musician/{musician_id}")
async def get_musician_by_id(
    musician_id: int,
    response: Response,
    musician_services: MusicianServices = Depends(get_musician_services)
) -> MusicianDTO | NotFoundMusicianError:
    try:
        return await musician_services.get_musician_by_id(musician_id)
    except MusicianNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundMusicianError()


@router.patch("/update-musician/{musician_id}")
async def update_musician(
    musician_id: int,
    musician: UpdateMusicianRequest,
    response: Response,
    musician_services: MusicianServices = Depends(get_musician_services),
) -> MusicianDTO | NotFoundMusicianError:
    try:
        return await musician_services.update_musician(UpdateMusicianDTO(id=musician_id, **musician.dict()))
    except MusicianNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundMusicianError()


@router.delete("/delete-musician/{musician_id}")
async def delete_musician(
    musician_id: int,
    response: Response,
    musician_services: MusicianServices = Depends(get_musician_services),
) -> MusicianDeleteResponse | NotFoundMusicianError:
    try:
        await musician_services.delete_musician(musician_id)
        response.status_code = status.HTTP_204_NO_CONTENT
        return MusicianDeleteResponse()
    except MusicianNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundMusicianError()
