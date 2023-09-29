import pytest
from aiogram import Bot, Dispatcher
from aiogram_dialog.test_tools import BotClient

from tests.fixtures.user_constants import create_tg_user


@pytest.fixture
def user_client(dp: Dispatcher, bot: Bot):
    client = BotClient(dp, bot=bot)
    client.user = create_tg_user()
    return client
