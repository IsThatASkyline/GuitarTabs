from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from guitar_app.presentation.tgbot import states


async def select_song(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["song_id"] = int(item_id)
    data["mod_value"] = 0
    await manager.switch_to(states.AllSongsPanelSG.song_menu)


async def select_song_tab(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.dialog_data
    data["tab_id"] = int(item_id)
    await manager.switch_to(states.AllSongsPanelSG.song_tab_detail)
