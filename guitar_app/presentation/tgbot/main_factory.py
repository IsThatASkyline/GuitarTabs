from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog.manager.message_manager import MessageManager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from guitar_app.presentation.tgbot.handlers import setup_handlers
from guitar_app.presentation.tgbot.middlewares import setup_middlewares


def create_bot(token) -> Bot:
    return Bot(
        token=token,
    )


def create_dispatcher(
    pool: async_sessionmaker[AsyncSession],
    message_manager: MessageManager,
) -> Dispatcher:
    dp = create_only_dispatcher()
    setup_middlewares(
        dp=dp,
        pool=pool,
    )
    setup_handlers(dp, message_manager)
    return dp


def create_only_dispatcher():
    dp = Dispatcher(
        storage=MemoryStorage(),
    )
    return dp
