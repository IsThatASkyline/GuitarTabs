from fastapi import APIRouter
from src.presentation.api.controllers.user import router as user_router
from src.presentation.api.controllers.musician import router as musician_router
from src.presentation.api.controllers.song import router as song_router
from src.presentation.api.controllers.band import router as band_router


def setup_controllers(router: APIRouter) -> None:
    router.include_router(user_router)
    router.include_router(musician_router)
    router.include_router(song_router)
    router.include_router(band_router)
