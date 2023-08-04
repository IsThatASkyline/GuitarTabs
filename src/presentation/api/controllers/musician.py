from fastapi import APIRouter, Response, status
from fastapi.params import Depends
from src.domain.guitarapp.dto import CreateMusicianDTO, MusicianDTO, UpdateMusicianDTO
from src.domain.guitarapp.exceptions import MusicianNotExists
from src.domain.guitarapp.services import MusicianServices
from src.presentation.api.controllers.requests import (
    CreateMusicianRequest,
    UpdateMusicianRequest,
)
from src.presentation.api.controllers.responses import MusicianDeleteResponse
from src.presentation.api.controllers.responses.exceptions import NotFoundMusicianError
from src.presentation.api.di.providers.services import get_musician_services


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
    musician_id: int, musician_services: MusicianServices = Depends(get_musician_services)
) -> MusicianDTO | NotFoundMusicianError:
    try:
        return await musician_services.get_musician_by_id(musician_id)
    except MusicianNotExists:
        return NotFoundMusicianError()


@router.patch("/update-musician/{musician_id}")
async def update_musician(
    musician_id: int,
    musician: UpdateMusicianRequest,
    musician_services: MusicianServices = Depends(get_musician_services),
) -> MusicianDTO:
    return await musician_services.update_musician(UpdateMusicianDTO(id=musician_id, **musician.dict()))


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
