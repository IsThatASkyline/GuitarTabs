from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from aiogram import Dispatcher
from aiogram_dialog.test_tools import MockMessageManager
# from aiogram_tests.mocked_bot import MockedBot
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import close_all_sessions, sessionmaker

from guitar_app.config import get_settings
from guitar_app.presentation.tgbot.handlers import setup_handlers
from guitar_app.presentation.tgbot.main_factory import create_only_dispatcher
from guitar_app.presentation.tgbot.middlewares import setup_middlewares


@pytest_asyncio.fixture
async def session(pool: sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with pool() as session_:
        yield session_


@pytest.fixture(scope="session")
def pool() -> Generator[sessionmaker, None, None]:
    engine = create_async_engine(url=get_settings().TEST_DB_URL)
    pool_: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    yield pool_  # type: ignore[misc]
    close_all_sessions()


@pytest.fixture(scope="session")
def dp(
    pool: async_sessionmaker[AsyncSession],
    message_manager: MockMessageManager,
) -> Dispatcher:
    dp = create_only_dispatcher()
    setup_handlers(dp, message_manager)
    setup_middlewares(
        dp=dp,
        pool=pool,
    )
    return dp


# @pytest.fixture
# def bot():
#     return MockedBot(token=get_settings().BOT_TOKEN)
#

@pytest.fixture(scope="session")
def message_manager():
    return MockMessageManager()
