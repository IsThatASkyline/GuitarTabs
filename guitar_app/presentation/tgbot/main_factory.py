from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog.manager.message_manager import MessageManager
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from guitar_app.config import Settings
from guitar_app.presentation.tgbot.handlers import setup_handlers
from guitar_app.presentation.tgbot.middlewares import setup_middlewares


def create_bot(token) -> Bot:
    return Bot(
        token=token,
        parse_mode=ParseMode.HTML,
    )


def create_dispatcher(
    pool: async_sessionmaker[AsyncSession],
    config: Settings,
    message_manager: MessageManager,
) -> Dispatcher:
    dp = create_only_dispatcher(config)
    bg_manager_factory = setup_handlers(dp, message_manager)
    setup_middlewares(
        dp=dp,
        pool=pool,
        bg_manager_factory=bg_manager_factory,
    )
    return dp


def create_only_dispatcher(config: Settings):

    dp = Dispatcher(
        storage=create_storage(config),
    )
    return dp


def create_storage(config) -> BaseStorage:
    # logger.info("creating storage for type %s", config.type_)
    match config.storage_type:
        # case StorageType.memory:
        case "memory":
            return MemoryStorage()
        # case StorageType.redis:
        case "redis":
            if config.REDIS_URL is None:
                raise ValueError("you have to specify redis config for use redis storage")
            return RedisStorage(
                create_redis(config), key_builder=DefaultKeyBuilder(with_destiny=True)
            )
        case _:
            raise NotImplementedError


def create_redis(config: Settings) -> Redis:
    # logger.info("created redis for %s", config)
    return Redis(host=config.REDIS_URL, port=config.REDIS_PORT, db=config.REDIS_DB)
