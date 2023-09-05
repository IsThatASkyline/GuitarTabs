from aiogram import Router
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.protocols import MessageManagerProtocol

from guitar_app.presentation.tgbot.dialogs import (
    main_menu,
    starters,
    band_manage,
)
from guitar_app.presentation.tgbot.dialogs import song_manage


def setup(message_manager: MessageManagerProtocol) -> Router:
    dialogs_router = Router(name=__name__)

    dialogs_router.include_router(starters.setup())
    dialogs_router.include_router(setup_all_dialogs())

    setup_dialogs(dialogs_router, message_manager=message_manager)
    return dialogs_router


def setup_all_dialogs() -> Router:
    router = Router(name=__name__ + ".common")

    main_menu.setup(router)
    song_manage.setup(router)
    band_manage.setup(router)

    return router
