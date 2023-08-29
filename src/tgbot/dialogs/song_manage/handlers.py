from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from src.application.guitarapp import services, dto
from src.infrastructure.db.uow import UnitOfWork

from src.tgbot import states


async def select_song(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["song_id"] = int(item_id)
    await manager.switch_to(states.AllSongsPanelSG.song_menu)


async def show_chords(c: CallbackQuery, widget: Any, manager: DialogManager):
    # await c.answer()
    # song_id = manager.dialog_data["song_id"]
    # await manager.start(states.FavoriteSongsPanelSG.chords, data={"song_id": song_id})
    pass


async def remove_song_from_favorites(c: CallbackQuery, widget: Any, manager: DialogManager):
    # await c.answer()
    # song_id = manager.dialog_data["song_id"]
    # user: dto.UserDTO = manager.middleware_data["user"]
    # uow: UnitOfWork = manager.middleware_data["uow"]
    # await ser
    # await manager.start(states.FavoriteSongsPanelSG.song, data={"song_id": song_id})
    pass