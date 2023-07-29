from fastapi import APIRouter
from guitar_app.src.presentation.api.controllers.user import router as user_router
from guitar_app.src.presentation.api.controllers.musician import router as musician_router


def setup_controllers(router: APIRouter) -> None:
    router.include_router(user_router)
    router.include_router(musician_router)