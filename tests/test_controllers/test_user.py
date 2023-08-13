import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_get_user_favorite_songs(
        client: AsyncClient,
        create_song_in_database,
        song_data,
        create_band_in_database,
        band_data,
        add_song_to_favorites_in_database,
        user_data,
        create_user_in_database,
        add_song_to_favorites_data
) -> None:
    await create_band_in_database(**band_data)
    await create_user_in_database(**user_data)
    await create_song_in_database(**song_data)
    await add_song_to_favorites_in_database(**add_song_to_favorites_data)

    response = await client.get(f'user/get-user-favorite-songs/{user_data["user_id"]}')

    r_data = response.json()

    assert len(r_data) == 1
    assert r_data[0]['title'] == song_data['title']
