import pytest
import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker

from src.infrastructure.db.models import Band, Musician, Song


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
        lyrics: str
    ):
        async with db_session_test() as session:
            await session.execute(
                insert(Song).values(
                    id=song_id,
                    title=title,
                    band_id=band_id,
                    lyrics=lyrics
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
        'lyrics': 'string'
    }
