from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog import BgManagerFactory
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.presentation.tgbot.utils.data import MiddlewareData


class InitMiddleware(BaseMiddleware):
    def __init__(
        self,
        pool: async_sessionmaker[AsyncSession],
        bg_manager_factory: BgManagerFactory,
    ):
        self.pool = pool
        self.bg_manager_factory = bg_manager_factory

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, Mapping[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        async with self.pool() as session:
            uow = UnitOfWork(session)
            data["uow"] = uow
            data["bg_manager_factory"] = self.bg_manager_factory
            result = await handler(event, data)
            del data["uow"]
        return result
