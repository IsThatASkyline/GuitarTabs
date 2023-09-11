from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from guitar_app.application.guitar import dto, services
from guitar_app.application.guitar.exceptions import SongNotExists
from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.presentation.tgbot import states


async def select_song(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["song_id"] = int(item_id)
    await manager.switch_to(states.AllSongsPanelSG.song_menu)


async def select_song_founded_by_title(
    c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str
):
    await c.answer()
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["song_id"] = int(item_id)
    await manager.switch_to(states.FoundedSongsPanelSG.song_menu)


async def select_song_by_band(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["song_id"] = int(item_id)
    await manager.switch_to(states.BandSongsPanelSG.song_menu)


async def select_favorite_song(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await c.answer()
    data = manager.dialog_data
    if not isinstance(data, dict):
        data = {}
    data["song_id"] = int(item_id)
    await manager.switch_to(states.FavoriteSongsPanelSG.song_menu)


async def add_song_to_favorite(c: CallbackQuery, widget: Button, manager: DialogManager):
    await c.answer()
    song_id = manager.dialog_data["song_id"]
    user: dto.UserDTO = manager.middleware_data["user"]
    uow: UnitOfWork = manager.middleware_data["uow"]
    try:
        await services.SongServices(uow).add_song_to_favorite(
            dto.FavoriteSongDTO(song_id=song_id, user_id=user.telegram_id)
        )
    except SongNotExists:
        return


async def remove_song_from_favorite(c: CallbackQuery, widget: Button, manager: DialogManager):
    await c.answer()
    song_id = manager.dialog_data["song_id"]
    user: dto.UserDTO = manager.middleware_data["user"]
    uow: UnitOfWork = manager.middleware_data["uow"]
    try:
        return await services.SongServices(uow).remove_song_from_favorite(
            dto.FavoriteSongDTO(song_id=song_id, user_id=user.telegram_id)
        )
    except SongNotExists:
        return


async def find_song_by_title(m: Message, dialog: Any, manager: DialogManager):
    if not m.text:
        await manager.switch_to(states.FoundedSongsPanelSG.message_type_error)
    else:
        data = manager.dialog_data
        if not isinstance(data, dict):
            data = {}
        data["song_title"] = m.text.strip()
        await manager.switch_to(states.FoundedSongsPanelSG.choose_song)
