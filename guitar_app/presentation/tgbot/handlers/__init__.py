import logging

from aiogram import Dispatcher
from aiogram_dialog import BgManagerFactory
from aiogram_dialog.api.protocols import MessageManagerProtocol

from guitar_app.presentation.tgbot import dialogs

from guitar_app.presentation.tgbot.handlers import base, errors

logger = logging.getLogger(__name__)


def setup_handlers(dp: Dispatcher, message_manager: MessageManagerProtocol) -> BgManagerFactory:
    errors.setup(dp)  # Bug with aiogram_dialog library
    dp.include_router(base.setup())

    bg_manager_factory = dialogs.setup(dp, message_manager)
    logger.info("handlers configured successfully")
    return bg_manager_factory
