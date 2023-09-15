from aiogram import Bot, Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.types.error_event import ErrorEvent
from aiogram_dialog import DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent


async def clear_unknown_intent(error: ErrorEvent, bot: Bot):
    assert error.update.callback_query
    assert error.update.callback_query.message
    await bot.edit_message_reply_markup(
        chat_id=error.update.callback_query.message.chat.id,
        message_id=error.update.callback_query.message.message_id,
        reply_markup=None,
    )


def setup(dp: Dispatcher):
    dp.errors.register(clear_unknown_intent, ExceptionTypeFilter(UnknownIntent))
