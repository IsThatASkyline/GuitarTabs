from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from src.application.guitarapp import services, dto
from src.infrastructure.db.uow import UnitOfWork

from src.tgbot import states


async def select_band(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["song_id"] = int(item_id)
    await manager.switch_to(states.AllBandsPanelSG.band_songs)


async def select_song(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["song_id"] = int(item_id)
    await manager.switch_to(states.AllBandsPanelSG.band_song)