import asyncio

from aiogram_dialog.manager.message_manager import MessageManager

from guitar_app.config import get_settings
from guitar_app.infrastructure.db.main import build_sessions, create_engine
from guitar_app.presentation.tgbot.main_factory import create_bot, create_dispatcher


async def main():
    config = get_settings()
    engine = create_engine(config.DB_URL)
    pool = build_sessions(engine)
    bot = create_bot(config.BOT_TOKEN)
    dp = create_dispatcher(pool=pool, config=config, message_manager=MessageManager())
    try:
        print("Started")
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types(skip_events={"aiogd_update"})
        )
    finally:
        print("Stopped")


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
