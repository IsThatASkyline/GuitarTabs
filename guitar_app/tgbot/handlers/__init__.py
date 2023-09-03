from aiogram import Dispatcher
from aiogram_dialog.api.protocols import MessageManagerProtocol

from guitar_app.tgbot import dialogs

from guitar_app.tgbot.handlers import base


def setup_handlers(dp: Dispatcher, message_manager: MessageManagerProtocol):
    dp.include_router(base.setup())

    dp.include_router(dialogs.setup(message_manager))
