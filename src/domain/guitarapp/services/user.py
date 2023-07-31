from src.domain.guitarapp.dto.user import CreateUserDTO, UpdateUserDTO, UserDTO
from src.domain.guitarapp.exceptions import UserNotExists
from src.domain.guitarapp.usecases import UserUseCase
from src.infrastructure.db.uow import UnitOfWork


class CreateUser(UserUseCase):
    async def __call__(self, user_dto: CreateUserDTO) -> UserDTO:
        user = await self.uow.app_holder.user_repo.create_user(user_dto)
        await self.uow.commit()
        return user


class GetUserById(UserUseCase):
    async def __call__(self, id_: int) -> UserDTO:
        user = await self.uow.app_holder.user_repo.get_user_by_id(id_)
        return user


class GetUsers(UserUseCase):
    async def __call__(self) -> list[UserDTO]:
        users = await self.uow.app_holder.user_repo.get_all_users()
        return users


class UpdateUser(UserUseCase):
    async def __call__(self, user_update_dto: UpdateUserDTO) -> None:
        await self.uow.app_holder.user_repo.update_user(
            user_update_dto.id,
            **user_update_dto.dict(exclude_none=True, exclude=set("id"))
        )
        await self.uow.commit()


class DeleteUser(UserUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.user_repo.get_user_by_id(id_):
            await self.uow.app_holder.user_repo.delete_user(id_)
            await self.uow.commit()
            return
        raise UserNotExists


class UserServices:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_user(self, user_dto: CreateUserDTO) -> UserDTO:
        return await CreateUser(self.uow)(user_dto)

    async def get_user_by_id(self, id_: int) -> UserDTO:
        return await GetUserById(self.uow)(id_)

    async def get_all_users(self) -> list[UserDTO]:
        return await GetUsers(self.uow)()

    async def update_user(self, update_user_dto: UpdateUserDTO) -> UserDTO:
        await UpdateUser(self.uow)(update_user_dto)
        return await GetUserById(self.uow)(update_user_dto.id)

    async def delete_user(self, id_: int) -> None:
        await DeleteUser(self.uow)(id_)