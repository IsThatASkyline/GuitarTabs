import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_all_bands(
    client: AsyncClient,
    band_data,
    create_band_in_database,
) -> None:
    await create_band_in_database(**band_data)

    response = await client.get("band/get-all-bands")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list) is True
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == band_data["band_id"]
    assert response.json()[0]["title"] == band_data["title"]


@pytest.mark.asyncio
async def test_get_band(client: AsyncClient, create_band_in_database, band_data) -> None:
    await create_band_in_database(**band_data)

    response = await client.get(f'band/get-band/{band_data["band_id"]}')
    response_404 = await client.get("band/get-band/123")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == band_data["title"]

    assert response_404.json()["detail"] == "Not found band"
    assert response_404.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_band(client: AsyncClient, band_data) -> None:
    data_json = {
        "id": band_data["band_id"],
        "title": band_data["title"],
    }
    response = await client.post("band/create-band", json=data_json)

    r_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert r_data["title"] == data_json["title"]


@pytest.mark.asyncio
async def test_update_band(client: AsyncClient, create_band_in_database, band_data) -> None:
    await create_band_in_database(**band_data)

    data_json = {"title": "new_string"}

    response = await client.patch(f'band/update-band/{band_data["band_id"]}', json=data_json)
    response_404 = await client.patch("band/update-band/123123123", json=data_json)

    r_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert r_data["title"] == data_json["title"]
    assert response_404.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_band(client: AsyncClient, create_band_in_database, band_data) -> None:
    await create_band_in_database(**band_data)

    response = await client.delete(f'band/delete-band/{band_data["band_id"]}')
    response_404 = await client.get(f'band/get-band/{band_data["band_id"]}')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response_404.json()["detail"] == "Not found band"
    assert response_404.status_code == status.HTTP_404_NOT_FOUND
