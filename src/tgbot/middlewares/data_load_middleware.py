from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from src.application.guitarapp import dto
from src.application.guitarapp import services
from src.infrastructure.db.uow import UnitOfWork

from src.tgbot.utils.data import MiddlewareData


class LoadDataMiddleware(BaseMiddleware):
    async def __call__(  # type: ignore
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        uow = data["uow"]
        if isinstance(event, Update):
            if user_tg := data.get("event_from_user", None):
                user = await services.UserServices(uow).get_user_by_id(user_tg.id)
            else:
                user = None
        else:
            user = await save_user(data, uow)
        data["user"] = user
        result = await handler(event, data)
        return result


async def save_user(data: MiddlewareData, uow: UnitOfWork) -> dto.UserDTO | None:
    user = data.get("event_from_user", None)
    if not user:
        return None
    return await services.UserServices(uow).create_user(dto.CreateUserDTO(telegram_id=user.id))
