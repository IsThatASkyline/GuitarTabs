from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager

from guitar_app.presentation.tgbot import states


async def select_song_founded_by_title(
    c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str
):
    await c.answer()
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["song_id"] = int(item_id)
    data['mod_value'] = 0
    await manager.switch_to(states.FoundedSongsPanelSG.song_menu)


async def select_founded_song_tab(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.dialog_data
    data["tab_id"] = int(item_id)
    await manager.switch_to(states.FoundedSongsPanelSG.song_tab_detail)


async def find_song_by_title(m: Message, dialog: Any, manager: DialogManager):
    if not m.text:
        await manager.switch_to(states.FoundedSongsPanelSG.message_type_error)
    else:
        data = manager.dialog_data
        if not isinstance(data, dict):
            data = {}
        data["song_title"] = m.text.strip()
        await manager.switch_to(states.FoundedSongsPanelSG.choose_song)
