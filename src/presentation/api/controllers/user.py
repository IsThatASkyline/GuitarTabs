from fastapi import APIRouter, Response, status
from fastapi.params import Depends
from src.application.guitarapp.dto import CreateUserDTO, UpdateUserDTO, UserDTO, SongDTO
from src.application.guitarapp.exceptions import UserNotExists
from src.application.guitarapp.services import UserServices
from src.presentation.api.controllers.requests.user import (
    CreateUserRequest,
    UpdateUserRequest,
)
from src.presentation.api.controllers.responses import UserDeleteResponse
from src.presentation.api.controllers.responses.exceptions import NotFoundUserError
from src.presentation.api.di.providers.services import get_user_services


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


@router.patch("/update-user/{user_id}")
async def update_user(
    user_id: int,
    user: UpdateUserRequest,
    user_services: UserServices = Depends(get_user_services),
) -> UserDTO:
    return await user_services.update_user(UpdateUserDTO(id=user_id, **user.dict()))


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