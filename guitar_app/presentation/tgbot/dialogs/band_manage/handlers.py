from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from guitar_app.presentation.tgbot import states


async def select_band(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    await manager.start(states.BandSongsPanelSG.choose_song, data={"band_id": int(item_id)})
