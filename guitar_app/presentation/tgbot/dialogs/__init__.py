from aiogram import Router, F
from aiogram.enums import ChatType
from aiogram_dialog import setup_dialogs, BgManagerFactory
from aiogram_dialog.api.protocols import MessageManagerProtocol

from guitar_app.presentation.tgbot.dialogs import (
    main_menu,
    starters,
    band_manage,
)
from guitar_app.presentation.tgbot.dialogs import song_manage


def setup(router: Router, message_manager: MessageManagerProtocol) -> BgManagerFactory:
    dialogs_router = Router(name=__name__)
    dialogs_router.message.filter(F.chat.type == ChatType.PRIVATE)

    dialogs_router.include_router(starters.setup())
    dialogs_router.include_router(setup_all_dialogs())

    bg_manager = setup_dialogs(dialogs_router, message_manager=message_manager)
    router.include_router(dialogs_router)
    return bg_manager


def setup_all_dialogs() -> Router:
    router = Router(name=__name__ + ".common")

    main_menu.setup(router)
    song_manage.setup(router)
    band_manage.setup(router)

    return router
