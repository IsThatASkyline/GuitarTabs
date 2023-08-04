import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_get_all_songs(
        client: AsyncClient,
        song_data,
        create_song_in_database,
        band_data,
        create_band_in_database
) -> None:
    await create_band_in_database(**band_data)
    await create_song_in_database(**song_data)

    response = await client.get('song/get-all-songs')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list) is True
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == 1
    assert response.json()[0]['title'] == song_data['title']
    assert response.json()[0]['band_id'] == song_data['band_id']


@pytest.mark.asyncio
async def test_get_song(
        client: AsyncClient,
        create_song_in_database,
        song_data,
        create_band_in_database,
        band_data
) -> None:
    await create_band_in_database(**band_data)
    await create_song_in_database(**song_data)

    response = await client.get(f'song/get-song/{song_data["song_id"]}')
    response_404 = await client.get('song/get-song/123')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['title'] == song_data['title']
    assert response.json()['band_id'] == song_data['band_id']
    assert response.json()['lyrics'] == song_data['lyrics']

    assert response_404.json()['detail'] == 'Not found song'
    # assert response_404.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_song(
        client: AsyncClient,
        create_song_in_database,
        create_band_in_database,
        band_data
) -> None:
    await create_band_in_database(**band_data)

    data_json = {
        'title': 'title',
        'band_id': band_data['band_id']
    }

    response = await client.post('song/create-song', json=data_json)
    r_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert r_data['title'] == data_json['title']
    assert r_data['band_id'] == data_json['band_id']


@pytest.mark.asyncio
async def test_update_song(
        client: AsyncClient,
        create_song_in_database,
        song_data,
        create_band_in_database,
        band_data
) -> None:
    await create_band_in_database(**band_data)
    await create_song_in_database(**song_data)

    data_json = {
        'title': 'new_title',
        'lyrics': 'new_lyrics',
    }
    response = await client.patch(f'song/update-song/{song_data["song_id"]}', json=data_json)
    r_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert r_data['title'] == data_json['title']
    assert r_data['lyrics'] == data_json['lyrics']


@pytest.mark.asyncio
async def test_delete_song(
        client: AsyncClient,
        create_song_in_database,
        song_data,
        create_band_in_database,
        band_data
) -> None:
    await create_band_in_database(**band_data)
    await create_song_in_database(**song_data)

    response = await client.delete(f'song/delete-song/{song_data["song_id"]}')

    assert response.status_code == status.HTTP_204_NO_CONTENT
