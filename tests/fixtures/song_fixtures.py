import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker

from guitar_app.infrastructure.db.models import Song, Verse, UserFavorite


@pytest_asyncio.fixture(scope='function')
async def create_song_in_database(db_session_test: sessionmaker):
    async def create_song_in_database_wrap(
        song_id: int,
        title: str,
        band_id: int,
        verses
    ):
        async with db_session_test() as session:
            await session.execute(
                insert(Song).values(
                    id=song_id,
                    title=title,
                    band_id=band_id,
                )
            )

            for verse in verses:
                await session.execute(
                    insert(Verse).values(
                        song_id=song_id,
                        title=verse['title'],
                        lyrics=verse['lyrics'],
                        chords=verse['chords'],
                    )
                )
            await session.commit()

    return create_song_in_database_wrap


@pytest_asyncio.fixture(scope='function')
async def song_data():
    return {
        'song_id': 1,
        'title': 'string',
        'band_id': 1,
        'verses': [
                {
                    'title': 'verse1',
                    'lyrics': 'lyrics',
                    'chords': 'Am C Dm G'
                },
                {
                    'title': 'verse2',
                    'lyrics': 'lyrics',
                    'chords': 'A Cm D Gm'
                },
            ],
    }


@pytest_asyncio.fixture(scope='function')
async def song_data2():
    return {
        'song_id': 2,
        'title': 'somestring',
        'band_id': 1,
        'verses': [
                {
                    'title': 'verse1',
                    'lyrics': 'lyrics',
                    'chords': 'Am C Dm G'
                },
                {
                    'title': 'verse2',
                    'lyrics': 'lyrics',
                    'chords': 'A Cm D Gm'
                },
            ],
    }


@pytest_asyncio.fixture(scope='function')
async def modulate_song_data1():
    return {
        'song_id': 1,
        'value': 1,
    }


@pytest_asyncio.fixture(scope='function')
async def modulate_song_data2():
    return {
        'song_id': 1,
        'value': -2
    }


@pytest_asyncio.fixture(scope='function')
async def after_modulate_song_data1():
    return {
        'id': 1,
        'title': 'string',
        'band': {
                'id': 1,
                'title': 'test_band',
            },
        'verses': [
                {
                    'title': 'verse1',
                    'lyrics': 'lyrics',
                    'chords': 'A#m C# D#m G#'
                },
                {
                    'title': 'verse2',
                    'lyrics': 'lyrics',
                    'chords': 'A# C#m D# G#m'
                },
            ],
    }


@pytest_asyncio.fixture(scope='function')
async def after_modulate_song_data2():
    return {
        'id': 1,
        'title': 'string',
        'band': {
                'id': 1,
                'title': 'test_band',
            },
        'verses': [
                {
                    'title': 'verse1',
                    'lyrics': 'lyrics',
                    'chords': 'Gm A# Cm F'
                },
                {
                    'title': 'verse2',
                    'lyrics': 'lyrics',
                    'chords': 'G A#m C Fm'
                },
            ],
    }


@pytest_asyncio.fixture(scope='function')
async def add_song_to_favorites_in_database(db_session_test: sessionmaker):
    async def add_song_to_favorites_in_database_wrap(
        song_id: int,
        user_id: int,
    ):
        async with db_session_test() as session:
            await session.execute(
                insert(UserFavorite).values(
                    song_id=song_id,
                    user_id=user_id,
                )
            )
            await session.commit()

    return add_song_to_favorites_in_database_wrap


@pytest_asyncio.fixture(scope='function')
async def add_song_to_favorites_data():
    return {
        'user_id': 1,
        'song_id': 1,
    }
