from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager

from src.tgbot.views.commands import CANCEL_COMMAND


async def cancel_state(message: Message, state: FSMContext, dialog_manager: DialogManager):
    await dialog_manager.reset_stack(remove_keyboard=True)
    current_state = await state.get_state()
    if current_state is None:
        return
    # Cancel state and inform user about it
    await state.clear()
    # And remove keyboard (just in case)
    await message.reply(
        "Диалог прекращён, данные удалены", reply_markup=ReplyKeyboardRemove(remove_keyboard=True)
    )


def setup() -> Router:
    router = Router(name=__name__)
    router.message.register(cancel_state, Command(commands=CANCEL_COMMAND))
    return router