import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_get_all_bands(
        client: AsyncClient,
        band_data,
        create_band_in_database,
) -> None:
    await create_band_in_database(**band_data)

    response = await client.get('band/get-all-bands')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list) is True
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == band_data['band_id']
    assert response.json()[0]['title'] == band_data['title']


@pytest.mark.asyncio
async def test_get_band(
        client: AsyncClient,
        create_band_in_database,
        band_data
) -> None:
    await create_band_in_database(**band_data)

    response = await client.get(f'band/get-band/{band_data["band_id"]}')
    response_404 = await client.get('band/get-band/123')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == band_data['title']

    assert response_404.json()['detail'] == 'Not found band'
    # assert response_404.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_band(
        client: AsyncClient,
        create_band_in_database
) -> None:
    data_json = {
        'title': 'string'
    }
    response = await client.post('band/create-band', json=data_json)
    r_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert r_data['title'] == data_json['title']


@pytest.mark.asyncio
async def test_update_band(
        client: AsyncClient,
        create_band_in_database,
        band_data
) -> None:
    await create_band_in_database(**band_data)

    data_json = {
        'title': 'new_string'
    }

    response = await client.patch(f'band/update-band/{band_data["band_id"]}', json=data_json)
    r_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert r_data['title'] == data_json['title']


@pytest.mark.asyncio
async def test_delete_band(
        client: AsyncClient,
        create_band_in_database,
        band_data
) -> None:
    await create_band_in_database(**band_data)

    response = await client.delete(f'band/delete-band/{band_data["band_id"]}')

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_add_musician_to_band(
        client: AsyncClient,
        create_band_in_database,
        create_musician_in_database,
        band_data,
        musician_data
) -> None:
    await create_band_in_database(**band_data)
    await create_musician_in_database(**musician_data)

    data_json = {
        'musician_id': musician_data['musician_id']
    }

    response = await client.patch(f'band/add-musician-to-band/{band_data["band_id"]}', json=data_json)

    r_data = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert r_data['title'] == band_data['title']
    assert r_data['id'] == band_data['band_id']
    assert len(r_data['members']) == 1
    assert r_data['members'][0]['first_name'] == musician_data['first_name']
    assert r_data['members'][0]['last_name'] == musician_data['last_name']