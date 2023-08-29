import asyncio

from aiogram_dialog.manager.message_manager import MessageManager

from src.tgbot.main_factory import create_bot, create_dispatcher

TOKEN = "6241238975:AAHPYeeZxYlR0DcT8rR9uGPAGyoekrQiG7c"


async def main():
    bot = create_bot(TOKEN)
    dp = create_dispatcher(message_manager=MessageManager())
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