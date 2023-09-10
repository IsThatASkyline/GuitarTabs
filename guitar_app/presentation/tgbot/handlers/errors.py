from aiogram import Dispatcher, Bot
from aiogram.filters import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent
from aiogram_dialog import DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent


async def clear_unknown_intent(error: ErrorEvent, dialog_manager: DialogManager, bot: Bot):
    await dialog_manager.reset_stack(True)
    assert error.update.callback_query
    assert error.update.callback_query.message
    await bot.edit_message_reply_markup(
        chat_id=error.update.callback_query.message.chat.id,
        message_id=error.update.callback_query.message.message_id,
        reply_markup=None,
    )


def setup(dp: Dispatcher):
    dp.errors.register(clear_unknown_intent, ExceptionTypeFilter(UnknownIntent))
