from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import StartMode

from src.tgbot import states
from src.tgbot.utils.router import register_start_handler
from src.tgbot.views.commands import START_COMMAND


def setup() -> Router:
    router = Router(name=__name__)

    register_start_handler(
        Command(START_COMMAND),
        state=states.MainMenuSG.main,
        router=router,
        mode=StartMode.RESET_STACK,
    )
    return router
