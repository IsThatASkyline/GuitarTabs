from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from aiogram_dialog.api.exceptions import UnknownIntent
from sqlalchemy.exc import IntegrityError

from guitar_app.application.guitar import dto, services
from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.presentation.tgbot.utils.data import MiddlewareData


class LoadDataMiddleware(BaseMiddleware):
    async def __call__(  # type: ignore
        self,
        handler: Callable[[TelegramObject, Mapping[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: MiddlewareData,
    ) -> Any:
        uow = data["uow"]
        if isinstance(event, Update):
            try:
                user = await save_user(data, uow)
            except IntegrityError:
                if user_tg := data.get("event_from_user", None):
                    user = await services.UserServices(uow).get_user_by_id(user_tg.id)
                else:
                    user = None

        data["user"] = user
        result = await handler(event, data)
        return result


async def save_user(data: MiddlewareData, uow: UnitOfWork) -> dto.UserDTO | None:
    user = data.get("event_from_user", None)
    if not user:
        return None
    return await services.UserServices(uow).create_user(
        dto.CreateUserDTO(telegram_id=user.id, username=user.username)
    )
