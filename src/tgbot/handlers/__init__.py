from aiogram import Dispatcher
from aiogram_dialog.api.protocols import MessageManagerProtocol

from src.tgbot import dialogs

from src.tgbot.handlers import *
from src.tgbot.handlers import base


def setup_handlers(dp: Dispatcher, message_manager: MessageManagerProtocol):
    dp.include_router(base.setup())

    dp.include_router(dialogs.setup(message_manager))
