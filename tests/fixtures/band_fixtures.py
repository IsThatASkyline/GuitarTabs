import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker

from src.infrastructure.db.models import Band


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
