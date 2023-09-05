import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_musicians(
    client: AsyncClient,
    musician_data,
    create_musician_in_database,
) -> None:
    await create_musician_in_database(**musician_data)

    response = await client.get("musician/get-all-musicians")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list) is True
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["first_name"] == musician_data["first_name"]
    assert response.json()[0]["last_name"] == musician_data["last_name"]


@pytest.mark.asyncio
async def test_get_musician(client: AsyncClient, create_musician_in_database, musician_data) -> None:
    await create_musician_in_database(**musician_data)

    response = await client.get(f'musician/get-musician/{musician_data["musician_id"]}')
    response_404 = await client.get("musician/get-musician/123")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == musician_data["first_name"]
    assert response.json()["last_name"] == musician_data["last_name"]

    assert response_404.json()["detail"] == "Not found musician"
    assert response_404.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_musician(
    client: AsyncClient, create_musician_in_database, musician_data
) -> None:
    data_json = {
        "musician_id": musician_data["musician_id"],
        "first_name": musician_data["first_name"],
        "last_name": musician_data["last_name"],
    }
    response = await client.post("musician/create-musician", json=data_json)

    r_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert r_data["first_name"] == data_json["first_name"]
    assert r_data["last_name"] == data_json["last_name"]


@pytest.mark.asyncio
async def test_update_musician(
    client: AsyncClient, create_musician_in_database, musician_data
) -> None:
    await create_musician_in_database(**musician_data)

    data_json = {"first_name": "new_first_name", "last_name": "new_last_name"}
    response = await client.patch(
        f'musician/update-musician/{musician_data["musician_id"]}', json=data_json
    )
    response_404 = await client.patch("musician/update-musician/123123123", json=data_json)

    r_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert r_data["first_name"] == data_json["first_name"]
    assert r_data["last_name"] == data_json["last_name"]
    assert response_404.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_musician(
    client: AsyncClient, create_musician_in_database, musician_data
) -> None:
    await create_musician_in_database(**musician_data)

    response = await client.delete(f'musician/delete-musician/{musician_data["musician_id"]}')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = await client.get(f'musician/get-musician/{musician_data["musician_id"]}')
    assert response.json()["detail"] == "Not found musician"
    assert response.status_code == status.HTTP_404_NOT_FOUND
