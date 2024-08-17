import asyncio
import logging

from aiogram_dialog.manager.message_manager import MessageManager
from guitar_app.config import get_settings, setup_logging
from guitar_app.infrastructure.db.main import build_sessions, create_engine
from guitar_app.presentation.tgbot.main_factory import create_bot, create_dispatcher

logger = logging.getLogger(__name__)


async def main():
    setup_logging()
    config = get_settings()
    engine = create_engine(config.DB_URL)
    pool = build_sessions(engine)
    bot = create_bot(config.BOT_TOKEN)
    dp = create_dispatcher(pool=pool, config=config, message_manager=MessageManager())
    try:
        logger.info("Started")
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types(skip_events={"aiogd_update"})
        )
    finally:
        await engine.dispose()
        logger.info("stopped")


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
