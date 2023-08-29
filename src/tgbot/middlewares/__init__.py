from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .init_middleware import InitMiddleware


def setup_middlewares(
    dp: Dispatcher,
    pool: async_sessionmaker[AsyncSession],
):
    dp.update.middleware(
        InitMiddleware(
            pool=pool,
        )
    )
