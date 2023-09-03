import asyncio

from aiogram_dialog.manager.message_manager import MessageManager

from src.config import get_settings
from src.infrastructure.db.main import create_engine, build_sessions
from src.tgbot.main_factory import create_bot, create_dispatcher

TOKEN = "6241238975:AAGwfeWFEqiAqZxQVPneTElpH8RkuLXL8Ac"


async def main():
    engine = create_engine(get_settings().DB_URL)
    pool = build_sessions(engine)
    bot = create_bot(TOKEN)
    dp = create_dispatcher(pool=pool, message_manager=MessageManager())
    try:
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types(skip_events={"aiogd_update"})
        )
    finally:
        print('Stopped')


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
