import pytest
import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker

from src.infrastructure.db.models import Band, Musician, Song, Verse, User, UserFavorite


@pytest_asyncio.fixture(scope='function')
async def create_band_in_database(db_session_test: sessionmaker):
    async def create_band_in_database_wrap(
        band_id: int,
        title: str
    ):
        async with db_session_test() as session:
            await session.execute(
                insert(Band).values(
                    id=band_id,
                    title=title,
                )
            )
            await session.commit()

    return create_band_in_database_wrap


@pytest_asyncio.fixture(scope='function')
async def band_data():
    return {
        'band_id': 1,
        'title': 'test_band'
    }


@pytest_asyncio.fixture(scope='function')
async def create_musician_in_database(db_session_test: sessionmaker):
    async def create_musician_in_database_wrap(
        musician_id: int,
        first_name: str,
        last_name: str
    ):
        async with db_session_test() as session:
            await session.execute(
                insert(Musician).values(
                    id=musician_id,
                    first_name=first_name,
                    last_name=last_name
                )
            )
            await session.commit()

    return create_musician_in_database_wrap


@pytest_asyncio.fixture(scope='function')
async def musician_data():
    return {
        'musician_id': 1,
        'first_name': 'first_name',
        'last_name': 'last_name',
    }


@pytest_asyncio.fixture(scope='function')
async def musician_data2():
    return {
        'musician_id': 2,
        'first_name': '2first_name',
        'last_name': '2lastname',
    }


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
        'band_id': 1,
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
        'band_id': 1,
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
async def create_user_in_database(db_session_test: sessionmaker):
    async def create_user_in_database_wrap(
        user_id: int,
        username: str,
        email: str,
        password: str,
    ):
        async with db_session_test() as session:
            await session.execute(
                insert(User).values(
                    id=user_id,
                    username=username,
                    email=email,
                    password=password,
                )
            )
            await session.commit()

    return create_user_in_database_wrap


@pytest_asyncio.fixture(scope='function')
async def user_data():
    return {
        'user_id': 1,
        'username': 'username',
        'email': 'email',
        'password': 'password'
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
