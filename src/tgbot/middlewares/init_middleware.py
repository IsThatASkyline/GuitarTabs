from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from src.tgbot.utils.data import MiddlewareData
from src.infrastructure.db.uow import UnitOfWork


class InitMiddleware(BaseMiddleware):
    def __init__(
        self,
        pool: async_sessionmaker[AsyncSession],
    ):
        self.pool = pool

    async def __call__(  # type: ignore[override]
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        async with self.pool() as session:
            uow = UnitOfWork(session)
            data["uow"] = uow
            result = await handler(event, data)
            del data["uow"]
        return result
