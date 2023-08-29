from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from src.tgbot import states


async def select_song(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["song_id"] = int(item_id)
    await manager.switch_to(states.AllSongsPanelSG.song_menu)


async def select_song_by_band(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["song_id"] = int(item_id)
    await manager.switch_to(states.BandSongsPanelSG.song_menu)


async def show_chords(c: CallbackQuery, widget: Any, manager: DialogManager):
    # await c.answer()
    # song_id = manager.dialog_data["song_id"]
    # await manager.start(states.FavoriteSongsPanelSG.chords, data={"song_id": song_id})
    pass