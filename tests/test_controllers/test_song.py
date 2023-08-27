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
    assert response.json()[0]['band']['id'] == song_data['band_id']


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
    assert response.json()['band']['id'] == song_data['band_id']

    assert response_404.json()['detail'] == 'Not found song'
    assert response_404.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_song(
        client: AsyncClient,
        create_song_in_database,
        create_band_in_database,
        song_data,
        band_data
) -> None:
    await create_band_in_database(**band_data)

    data_json = {
        'id': song_data['song_id'],
        'title': song_data['title'],
        'band_id': song_data['band_id']
    }

    response = await client.post('song/create-song', json=data_json)

    r_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert r_data['title'] == data_json['title']
    assert r_data['id'] == data_json['band_id']


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
    }
    response = await client.patch(f'song/update-song/{song_data["song_id"]}', json=data_json)
    response_404 = await client.patch(f'song/update-song/123123123', json=data_json)

    r_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert r_data['title'] == data_json['title']
    assert response_404.status_code == status.HTTP_404_NOT_FOUND


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

    response = await client.get(f'song/get-song/{song_data["song_id"]}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == 'Not found song'


@pytest.mark.asyncio
async def test_modulate_song(
        client: AsyncClient,
        create_song_in_database,
        song_data,
        create_band_in_database,
        band_data,
        modulate_song_data1,
        modulate_song_data2,
        after_modulate_song_data1,
        after_modulate_song_data2
) -> None:
    await create_band_in_database(**band_data)
    await create_song_in_database(**song_data)

    data_json1 = {
        'value': modulate_song_data1['value'],
    }

    data_json2 = {
        'value': modulate_song_data2['value'],
    }

    response = await client.post(f'song/modulate-song/{modulate_song_data1["song_id"]}', json=data_json1)
    response2 = await client.post(f'song/modulate-song/{modulate_song_data2["song_id"]}', json=data_json2)
    response_404 = await client.post(f'song/modulate-song/123213', json=data_json2)

    assert response.json() == after_modulate_song_data1
    assert response2.json() == after_modulate_song_data2
    assert response_404.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_add_song_to_favorite(
        client: AsyncClient,
        create_song_in_database,
        song_data,
        band_data,
        user_data,
        create_band_in_database,
        create_user_in_database,
) -> None:
    await create_band_in_database(**band_data)
    await create_song_in_database(**song_data)
    await create_user_in_database(**user_data)

    data_json = {
        'user_id': user_data['user_id'],
    }

    response = await client.post(f'song/song-to-favorite/{song_data["song_id"]}', json=data_json)
    assert response.json()['detail'] == 'Песня добавлена в избранное'
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_remove_song_from_favorite(
        client: AsyncClient,
        create_song_in_database,
        song_data,
        band_data,
        user_data,
        create_band_in_database,
        create_user_in_database,
        add_song_to_favorites_data,
        add_song_to_favorites_in_database
) -> None:
    await create_band_in_database(**band_data)
    await create_song_in_database(**song_data)
    await create_user_in_database(**user_data)
    await add_song_to_favorites_in_database(**add_song_to_favorites_data)

    data_json = {
        'user_id': user_data['user_id'],
    }

    response = await client.post(f'song/song-to-favorite/{song_data["song_id"]}', json=data_json)

    assert response.json()['detail'] == 'Песня убрана из избранного'
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_find_song(
        client: AsyncClient,
        create_song_in_database,
        song_data,
        song_data2,
        band_data,
        create_band_in_database,
) -> None:
    await create_band_in_database(**band_data)
    await create_song_in_database(**song_data)
    await create_song_in_database(**song_data2)

    title_part1 = song_data['title'][0:2]
    data_json1 = {
        'value': title_part1,
    }

    title_part2 = song_data2['title'][0:2]
    data_json2 = {
        'value': title_part2,
    }

    response1 = await client.post(f'song/find-song', json=data_json1)
    r_data1 = response1.json()

    response2 = await client.post(f'song/find-song', json=data_json2)
    r_data2 = response2.json()

    assert len(r_data1) == 2
    assert title_part1 in r_data1[0]['title']
    assert title_part1 in r_data1[1]['title']
    assert r_data1[0]['band']['id'] == song_data['band_id']
    assert r_data1[0]['band']['id'] == song_data2['band_id']

    assert len(r_data2) == 1
    assert title_part2 in r_data2[0]['title']
    assert r_data2[0]['band']['id'] == song_data['band_id']
