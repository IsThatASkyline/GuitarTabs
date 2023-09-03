from fastapi import APIRouter, Response, status
from fastapi.params import Depends

from src.application.guitarapp.dto import CreateBandDTO, BandDTO, UpdateBandDTO, FullBandDTO, UpdateMusicianBandDTO
from src.application.guitarapp.exceptions import BandNotExists, MusicianNotExists
from src.application.guitarapp.services import BandServices
from src.presentation.api.controllers.requests import (
    CreateBandRequest,
    UpdateBandRequest,
    UpdateMusicianBandRequest,
)
from src.presentation.api.controllers.responses import BandDeleteResponse
from src.presentation.api.controllers.responses.exceptions import NotFoundBandError, NotFoundMusicianError
from src.presentation.api.di.providers.services import get_band_services

router = APIRouter(prefix="/band", tags=["band"])


@router.post("/create-band")
async def create_band(
    band: CreateBandRequest,
    response: Response,
    band_services: BandServices = Depends(get_band_services),
) -> FullBandDTO:
    response.status_code = status.HTTP_201_CREATED
    return await band_services.create_band(CreateBandDTO(**band.dict()))


@router.get("/get-all-bands")
async def get_all_bands(
    band_services: BandServices = Depends(get_band_services),
) -> list[BandDTO]:
    return await band_services.get_all_bands()


@router.get("/get-band/{band_id}")
async def get_band_by_id(
    band_id: int,
    response: Response,
    band_services: BandServices = Depends(get_band_services)
) -> FullBandDTO | NotFoundBandError:
    try:
        return await band_services.get_band_by_id(band_id)
    except BandNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundBandError()


@router.patch("/update-band/{band_id}")
async def update_band(
    band_id: int,
    response: Response,
    band: UpdateBandRequest,
    band_services: BandServices = Depends(get_band_services),
) -> FullBandDTO | NotFoundBandError:
    try:
        return await band_services.update_band(UpdateBandDTO(id=band_id, **band.dict()))
    except BandNotExists:
        response.status_code = response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundBandError()


@router.post("/add-musician-to-band/{band_id}")
async def add_musician_to_band(
    band_id: int,
    response: Response,
    band: UpdateMusicianBandRequest,
    band_services: BandServices = Depends(get_band_services),
) -> FullBandDTO | NotFoundBandError | NotFoundMusicianError:
    try:
        return await band_services.add_musician_to_band(UpdateMusicianBandDTO(band_id=band_id, **band.dict()))
    except BandNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundBandError()
    except MusicianNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundMusicianError()


@router.delete("/delete-band/{band_id}")
async def delete_band(
    band_id: int,
    response: Response,
    band_services: BandServices = Depends(get_band_services),
) -> BandDeleteResponse | NotFoundBandError:
    try:
        await band_services.delete_band(band_id)
        response.status_code = status.HTTP_204_NO_CONTENT
        return BandDeleteResponse()
    except BandNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundBandError()
