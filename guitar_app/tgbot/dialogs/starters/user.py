from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import StartMode

from guitar_app.tgbot import states
from guitar_app.tgbot.utils.router import register_start_handler
from guitar_app.tgbot.views.commands import START_COMMAND


def setup() -> Router:
    router = Router(name=__name__)

    register_start_handler(
        Command(START_COMMAND),
        state=states.MainMenuSG.main,
        router=router,
        mode=StartMode.RESET_STACK,
    )
    return router
