import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_users(
    client: AsyncClient,
    user_data,
    create_user_in_database,
) -> None:
    await create_user_in_database(**user_data)

    response = await client.get("user/get-all-users")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list) is True
    assert len(response.json()) == 1
    assert response.json()[0]["telegram_id"] == user_data["telegram_id"]
    assert response.json()[0]["username"] == user_data["username"]


@pytest.mark.asyncio
async def test_get_user(
    client: AsyncClient,
    user_data,
    create_user_in_database,
) -> None:
    await create_user_in_database(**user_data)
    response = await client.get(f'user/get-user/{user_data["telegram_id"]}')
    response_404 = await client.get("user/get-user/1223")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["telegram_id"] == user_data["telegram_id"]
    assert response.json()["username"] == user_data["username"]
    assert response_404.json()["detail"] == "Not found user"
    assert response_404.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_user(
    client: AsyncClient,
    user_data,
    create_user_in_database,
) -> None:
    await create_user_in_database(**user_data)

    response = await client.delete(f'user/delete-user/{user_data["telegram_id"]}')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.get(f'user/get-user/{user_data["telegram_id"]}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Not found user"
