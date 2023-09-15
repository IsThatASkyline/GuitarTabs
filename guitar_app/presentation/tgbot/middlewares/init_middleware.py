from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog.api.exceptions import UnknownIntent
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.presentation.tgbot.utils.data import MiddlewareData


class InitMiddleware(BaseMiddleware):
    def __init__(
        self,
        pool: async_sessionmaker[AsyncSession],
    ):
        self.pool = pool

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, Mapping[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        async with self.pool() as session:
            uow = UnitOfWork(session)
            data["uow"] = uow
            result = await handler(event, data)
            del data["uow"]
        return result
