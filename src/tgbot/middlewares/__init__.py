from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .init_middleware import InitMiddleware
from .data_load_middleware import LoadDataMiddleware


def setup_middlewares(
    dp: Dispatcher,
    pool: async_sessionmaker[AsyncSession],
):
    dp.update.middleware(
        InitMiddleware(
            pool=pool,
        )
    )
    dp.update.middleware(LoadDataMiddleware())
