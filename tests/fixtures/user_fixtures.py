import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker

from guitar_app.infrastructure.db.models import User


@pytest_asyncio.fixture(scope="function")
async def create_user_in_database(db_session_test: sessionmaker):
    async def create_user_in_database_wrap(
        user_id: int,
        telegram_id: int,
        username: str,
    ):
        async with db_session_test() as session:
            await session.execute(
                insert(User).values(
                    id=user_id,
                    username=username,
                    telegram_id=telegram_id,
                )
            )
            await session.commit()

    return create_user_in_database_wrap


@pytest_asyncio.fixture(scope="function")
async def user_data():
    return {
        "user_id": 1,
        "telegram_id": 121212,
        "username": 'Johnny Marr',
    }
