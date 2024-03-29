from fastapi import APIRouter, Response, status
from fastapi.params import Depends

from guitar_app.application.guitar.dto import (
    BandDTO,
    CreateBandDTO,
    FullBandDTO,
    UpdateBandDTO,
)
from guitar_app.application.guitar.exceptions import BandNotExists
from guitar_app.application.guitar.services import BandServices
from guitar_app.presentation.api.controllers.requests import (
    CreateBandRequest,
    UpdateBandRequest,
)
from guitar_app.presentation.api.controllers.responses import BandDeleteResponse
from guitar_app.presentation.api.controllers.responses.exceptions import (
    NotFoundBandError,
)
from guitar_app.presentation.api.di.providers.services import get_band_services

router = APIRouter(prefix="/band", tags=["band"])


@router.post("/create-band")
async def create_band(
    band: CreateBandRequest,
    response: Response,
    band_services: BandServices = Depends(get_band_services),
) -> BandDTO:
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
    band_services: BandServices = Depends(get_band_services),
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
