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
        create_band_in_database,
        band_data
) -> None:
    data_json = {
        'id': band_data['band_id'],
        'title': band_data['title'],
    }
    response_create = await client.post('band/create-band', json=data_json)
    response_get = await client.get(f'band/get-band/{band_data["band_id"]}')

    r_data = response_get.json()

    assert response_create.status_code == status.HTTP_201_CREATED
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

    response_update = await client.patch(f'band/update-band/{band_data["band_id"]}', json=data_json)
    response_get = await client.get(f'band/get-band/{band_data["band_id"]}')

    r_data = response_get.json()

    assert response_update.status_code == status.HTTP_200_OK
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

    response = await client.get(f'band/get-band/{band_data["band_id"]}')
    # assert response.text == 'Not found band'
    # assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_add_musician_to_band(
        client: AsyncClient,
        create_band_in_database,
        create_musician_in_database,
        band_data,
        musician_data,
        musician_data2
) -> None:
    await create_band_in_database(**band_data)
    await create_musician_in_database(**musician_data)
    await create_musician_in_database(**musician_data2)

    data_json = {
        'musician_id': musician_data['musician_id']
    }

    data_json2 = {
        'musician_id': musician_data2['musician_id']
    }

    await client.patch(f'band/add-musician-to-band/{band_data["band_id"]}', json=data_json)
    response = await client.patch(f'band/add-musician-to-band/{band_data["band_id"]}', json=data_json2)

    r_data = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert r_data['title'] == band_data['title']
    assert r_data['id'] == band_data['band_id']
    assert len(r_data['members']) == 2
    assert r_data['members'][0]['first_name'] == musician_data['first_name']
    assert r_data['members'][0]['last_name'] == musician_data['last_name']
    assert r_data['members'][1]['first_name'] == musician_data2['first_name']
    assert r_data['members'][1]['last_name'] == musician_data2['last_name']