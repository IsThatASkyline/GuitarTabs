from aiogram import Dispatcher
from aiogram_dialog import BgManagerFactory
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from .init_middleware import InitMiddleware
from .data_load_middleware import LoadDataMiddleware


def setup_middlewares(
    dp: Dispatcher,
    pool: async_sessionmaker[AsyncSession],
    bg_manager_factory: BgManagerFactory,
):
    dp.update.middleware(
        InitMiddleware(
            pool=pool,
            bg_manager_factory=bg_manager_factory,
        )
    )
    dp.update.middleware(LoadDataMiddleware())
