from typing import Any, Awaitable, Callable, Mapping

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from aiogram_dialog.api.exceptions import UnknownIntent
from sqlalchemy.exc import IntegrityError

from guitar_app.application.guitar import dto, services
from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.presentation.tgbot.utils.data import MiddlewareData

from aiogram_dialog.api.entities import DialogUpdate


class LoadDataMiddleware(BaseMiddleware):
    async def __call__(  # type: ignore
            self,
            handler: Callable[[TelegramObject, Mapping[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData,
    ) -> Any:
        try:
            uow = data["uow"]
            if user_tg := data.get("event_from_user", None):
                user = await services.UserServices(uow).get_user_by_id(user_tg.id)
            else:
                user = await save_user(data, uow)
            data["user"] = user
            result = await handler(event, data)
            return result
        except UnknownIntent:
            # In case, when bot been restarted and user press old menu buttons
            # Bug with aiogram_dialog library
            pass


async def save_user(data: MiddlewareData, uow: UnitOfWork) -> dto.UserDTO | None:
    user = data.get("event_from_user", None)
    if not user:
        return None
    return await services.UserServices(uow).create_user(
        dto.CreateUserDTO(telegram_id=user.id, username=user.username)
    )
