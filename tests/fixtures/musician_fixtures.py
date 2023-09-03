import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker

from src.infrastructure.db.models import Musician


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

