import pytest

from guitar_app.application.guitar.dto import CreateUserDTO, UserDTO
from guitar_app.application.guitar.exceptions import UserNotExists
from guitar_app.application.guitar.services import UserServices
from tests.mocks.repo import FakeUnitOfWork, FakeUserRepo


@pytest.mark.asyncio
async def test_create_user_service():
    user_data = CreateUserDTO(telegram_id=12345, username="Gorilla228")
    user = await UserServices(uow=FakeUnitOfWork()).create_user(user_data)
    assert user.username == user_data.username


@pytest.mark.asyncio
async def test_get_all_users_service():
    user_data_1 = UserDTO(telegram_id=12345, username="Gorilla228")
    user_data_2 = UserDTO(telegram_id=54321, username="Barracuda")
    repo = FakeUserRepo([user_data_1, user_data_2])
    users = await UserServices(uow=FakeUnitOfWork(user_repo=repo)).get_all_users()
    assert len(users) == 2
    assert users[0].username == user_data_1.username
    assert users[1].username == user_data_2.username


@pytest.mark.asyncio
async def test_get_user_by_id_service():
    user_data_1 = UserDTO(telegram_id=12345, username="Gorilla228")
    user_data_2 = UserDTO(telegram_id=54321, username="Barracuda")
    repo = FakeUserRepo([user_data_1, user_data_2])
    user = await UserServices(uow=FakeUnitOfWork(user_repo=repo)).get_user_by_id(2)
    assert user.username == user_data_2.username


@pytest.mark.asyncio
async def test_delete_user_service():
    user_data_1 = UserDTO(telegram_id=12345, username="Gorilla228")
    user_data_2 = UserDTO(telegram_id=54321, username="Barracuda")
    repo = FakeUserRepo([user_data_1, user_data_2])
    await UserServices(uow=FakeUnitOfWork(user_repo=repo)).delete_user(2)
    with pytest.raises(UserNotExists):
        await UserServices(uow=FakeUnitOfWork(user_repo=repo)).get_user_by_id(2)
