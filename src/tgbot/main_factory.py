from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog.manager.message_manager import MessageManager
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.tgbot.handlers import setup_handlers


def create_bot(token) -> Bot:
    return Bot(
        token=token,
    )


def create_dispatcher(
    message_manager: MessageManager,
) -> Dispatcher:
    dp = create_only_dispatcher()
    setup_handlers(dp, message_manager)
    return dp


def create_only_dispatcher():
    dp = Dispatcher(
        storage=MemoryStorage(),
    )
    return dp