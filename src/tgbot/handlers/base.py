from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import html_decoration as hd


async def chat_id(message: Message, chat: int, user: int):
    text = f"id этого чата: {hd.pre(str(chat))}\n" f"Ваш id: {hd.pre(user)}"
    await message.reply(text, disable_notification=True)


def setup() -> Router:
    router = Router(name=__name__)
    router.message.register(
        chat_id, Command(commands=["idchat"], prefix="/!")
    )

    return router