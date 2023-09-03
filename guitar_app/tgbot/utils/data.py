from typing import TypedDict, Any

from aiogram import types, Bot, Router
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import Stack, Context
from aiogram_dialog.context.storage import StorageProxy

from guitar_app.application.guitar import dto
from guitar_app.infrastructure.db.uow import UnitOfWork
# from shvatka.tgbot.config.models.bot import BotConfig


class AiogramMiddlewareData(TypedDict, total=False):
    event_from_user: types.User
    event_chat: types.Chat
    bot: Bot
    fsm_storage: BaseStorage
    state: FSMContext
    raw_state: Any
    handler: HandlerObject
    event_update: types.Update
    event_router: Router


class DialogMiddlewareData(AiogramMiddlewareData, total=False):
    dialog_manager: DialogManager
    aiogd_storage_proxy: StorageProxy
    aiogd_stack: Stack
    aiogd_context: Context


class MiddlewareData(DialogMiddlewareData, total=False):
    uow: UnitOfWork
    user: dto.UserDTO | None
