import asyncio
import os
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, close_all_sessions

from guitar_app.config import get_settings
from guitar_app.infrastructure.db.models.base import BaseAlchemyModels
from guitar_app.presentation.api.controllers import setup_controllers
from guitar_app.infrastructure.db.main import build_sessions, create_engine
from guitar_app.presentation.api.di import setup_di


db_engine = create_engine(get_settings().TEST_DB_URL)


def build_test_app() -> FastAPI:
    app = FastAPI()
    BaseAlchemyModels.metadata.bind = db_engine
    setup_di(app, build_sessions(db_engine))

    setup_controllers(app.router)

    return app


@pytest_asyncio.fixture(scope='session')
async def db_session_test() -> sessionmaker:
    yield build_sessions(db_engine)
    close_all_sessions()


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function', autouse=True)
async def clean_tables(db_session_test) -> None:
    tables = ('musician_table', 'song_table', 'musician_band_table', 'band_table', 'user_table', 'user_favorite_table')
    async with db_session_test() as session:
        for table in tables:
            statement = text(f"""TRUNCATE TABLE {table} CASCADE;""")
            await session.execute(statement)
            await session.commit()


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with db_engine.begin() as conn:
        await conn.run_sync(BaseAlchemyModels.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(BaseAlchemyModels.metadata.drop_all)


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=build_test_app(), base_url='http://test') as client_:
        yield client_


pytest_plugins = [
    'tests.fixtures.band_fixtures',
    'tests.fixtures.musician_fixtures',
    'tests.fixtures.song_fixtures',
    'tests.fixtures.user_fixtures',
]