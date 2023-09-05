from guitar_app.application.common.usecases.base import BaseUseCase
from guitar_app.application.guitar.dto import CreateUserDTO, UserDTO, UpdateUserDTO
from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.application.guitar.exceptions import UserNotExists


class UserUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)


class CreateUser(UserUseCase):
    async def __call__(self, user_dto: CreateUserDTO) -> UserDTO:
        user = await self.uow.app_holder.user_repo.add(user_dto)
        await self.uow.commit()
        return user


class GetUserById(UserUseCase):
    async def __call__(self, id_: int) -> UserDTO:
        user = await self.uow.app_holder.user_repo.get(id_)
        return user


class GetUsers(UserUseCase):
    async def __call__(self) -> list[UserDTO]:
        return await self.uow.app_holder.user_repo.list()


class UpdateUser(UserUseCase):
    async def __call__(self, user_update_dto: UpdateUserDTO) -> None:
        await self.uow.app_holder.user_repo.update(
            user_update_dto.id,
            **user_update_dto.dict(exclude_none=True, exclude=set("id"))
        )
        await self.uow.commit()


class DeleteUser(UserUseCase):
    async def __call__(self, id_: int) -> None:
        if await self.uow.app_holder.user_repo.get(id_):
            await self.uow.app_holder.user_repo.delete(id_)
            await self.uow.commit()
            return
        raise UserNotExists
