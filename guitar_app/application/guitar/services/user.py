from guitar_app.application.guitar.dto.user import CreateUserDTO, UpdateUserDTO, UserDTO
from guitar_app.application.guitar.usecases import (
    CreateUser,
    DeleteUser,
    GetUserById,
    GetUsers,
    UpdateUser,
)
from guitar_app.infrastructure.db.uow import UnitOfWork


class UserServices:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_user(self, user_dto: CreateUserDTO) -> UserDTO:
        async with self.uow:
            user = await CreateUser(self.uow)(user_dto)
            await self.uow.commit()
            return user

    async def get_user_by_id(self, id_: int) -> UserDTO:
        return await GetUserById(self.uow)(id_)

    async def get_all_users(self) -> list[UserDTO]:
        return await GetUsers(self.uow)()

    async def update_user(self, update_user_dto: UpdateUserDTO) -> UserDTO:
        async with self.uow:
            await UpdateUser(self.uow)(update_user_dto)
            await self.uow.commit()
            return await GetUserById(self.uow)(update_user_dto.id)

    async def delete_user(self, id_: int) -> None:
        async with self.uow:
            await DeleteUser(self.uow)(id_)
            await self.uow.commit()
