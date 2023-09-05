from fastapi import APIRouter, Response, status
from fastapi.params import Depends

from guitar_app.application.guitar.dto import CreateUserDTO, UserDTO
from guitar_app.application.guitar.exceptions import UserNotExists
from guitar_app.application.guitar.services import UserServices
from guitar_app.presentation.api.controllers.requests.user import CreateUserRequest
from guitar_app.presentation.api.controllers.responses import UserDeleteResponse
from guitar_app.presentation.api.controllers.responses.exceptions import (
    NotFoundUserError,
)
from guitar_app.presentation.api.di.providers.services import get_user_services

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/get-user/{user_id}")
async def get_user_by_id(
    user_id: int, user_services: UserServices = Depends(get_user_services)
) -> UserDTO:
    return await user_services.get_user_by_id(user_id)


@router.get("/get-all-users")
async def get_all_users(
    user_services: UserServices = Depends(get_user_services),
) -> list[UserDTO]:
    users = await user_services.get_all_users()
    return users


@router.post("/create-user")
async def create_user(
    user: CreateUserRequest,
    response: Response,
    user_services: UserServices = Depends(get_user_services),
) -> UserDTO:
    response.status_code = status.HTTP_201_CREATED
    return await user_services.create_user(CreateUserDTO(**user.dict()))


@router.delete("/delete-user/{user_id}")
async def delete_post(
    user_id: int,
    response: Response,
    user_services: UserServices = Depends(get_user_services),
) -> UserDeleteResponse | NotFoundUserError:
    try:
        await user_services.delete_user(user_id)
        response.status_code = status.HTTP_204_NO_CONTENT
        return UserDeleteResponse()
    except UserNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return NotFoundUserError()
