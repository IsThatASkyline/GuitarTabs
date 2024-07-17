import pytest
from aiogram_dialog.test_tools import BotClient, MockMessageManager
from aiogram_dialog.test_tools.keyboard import InlineButtonTextLocator
from aiogram_tests.mocked_bot import MockedBot

from guitar_app.presentation.tgbot.views.commands import START_COMMAND


@pytest.mark.asyncio
async def test_menu(
    user_client: BotClient,
    message_manager: MockMessageManager,
    bot: MockedBot,
    band_data,
    create_band_in_database,
    song_data,
    user_data,
    create_user_in_database,
    create_song_in_database,
    add_song_to_favorites_data,
    add_song_to_favorites_in_database,
):
    await create_band_in_database(**band_data)
    await create_song_in_database(**song_data)
    await create_user_in_database(**user_data)

    await user_client.send("/" + START_COMMAND.command)
    first_message = message_manager.one_message()
    assert first_message.text is not None
    assert "Ты находишься в главном меню." in first_message.text
    assert first_message.reply_markup
    assert "⭐️Избранные песни" in first_message.reply_markup.inline_keyboard[0][0].text
    assert "🎵Все песни" in first_message.reply_markup.inline_keyboard[1][0].text
    assert "🎸Все группы" in first_message.reply_markup.inline_keyboard[2][0].text
    assert "🔍Найти песню по названию" in first_message.reply_markup.inline_keyboard[3][0].text
    assert "🚪Закрыть" in first_message.reply_markup.inline_keyboard[4][0].text

    message_manager.reset_history()
    await user_client.click(first_message, InlineButtonTextLocator("🎵Все песни"))
    new_message = message_manager.one_message()
    assert new_message.text == "🎵Все песни"
    assert song_data["title"] in new_message.reply_markup.inline_keyboard[0][0].text
    await user_client.click(new_message, InlineButtonTextLocator("🔙Назад"))

    message_manager.reset_history()
    await user_client.click(first_message, InlineButtonTextLocator("⭐️Избранные песни"))
    new_message = message_manager.one_message()
    assert new_message.text == "⭐️Избранные песни"
    assert song_data["title"] not in new_message.reply_markup.inline_keyboard[0][0].text
    await user_client.click(new_message, InlineButtonTextLocator("🔙Назад"))

    await add_song_to_favorites_in_database(**add_song_to_favorites_data)

    message_manager.reset_history()
    await user_client.click(first_message, InlineButtonTextLocator("⭐️Избранные песни"))
    new_message = message_manager.one_message()
    assert new_message.text == "⭐️Избранные песни"
    assert song_data["title"] in new_message.reply_markup.inline_keyboard[0][0].text
    await user_client.click(new_message, InlineButtonTextLocator("🔙Назад"))

    message_manager.reset_history()
    await user_client.click(first_message, InlineButtonTextLocator("🎸Все группы"))
    new_message = message_manager.one_message()
    assert new_message.text == "🎸Все группы"
    assert band_data["title"] in new_message.reply_markup.inline_keyboard[0][0].text
    await user_client.click(new_message, InlineButtonTextLocator("🔙Назад"))

    message_manager.reset_history()
    await user_client.click(first_message, InlineButtonTextLocator("🔍Найти песню по названию"))
    new_message = message_manager.one_message()
    assert new_message.text == "🔍Введите название песни"
    message_manager.reset_history()
    wrong_song_name = "wrong_song_name"
    await user_client.send(wrong_song_name)
    new_message = message_manager.one_message()
    assert f"Песен с названием <b>{wrong_song_name}</b> не найдено" in new_message.text
    assert song_data["title"] not in new_message.reply_markup.inline_keyboard[0][0].text
    message_manager.reset_history()
    await user_client.click(new_message, InlineButtonTextLocator("🔙Назад"))

    message_manager.reset_history()
    await user_client.click(first_message, InlineButtonTextLocator("🔍Найти песню по названию"))
    new_message = message_manager.one_message()
    assert new_message.text == "🔍Введите название песни"
    message_manager.reset_history()
    await user_client.send(song_data["title"])
    new_message = message_manager.one_message()
    assert song_data["title"] in new_message.reply_markup.inline_keyboard[0][0].text
    assert f"Песни с названием: <b>{song_data['title']}</b> (Всего: <b>1</b>" in new_message.text
    message_manager.reset_history()
    await user_client.click(new_message, InlineButtonTextLocator("🔙Назад"))
