from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from guitar_app.application.guitar import dto, services
from guitar_app.application.guitar.exceptions import SongNotExists
from guitar_app.infrastructure.db.uow import UnitOfWork


async def refresh_mod_value(c: CallbackQuery, widget: Any, manager: DialogManager):
    await c.answer()
    data = manager.dialog_data
    data["mod_value"] = 0


async def up_key(c: CallbackQuery, widget: Any, manager: DialogManager):
    await c.answer()
    data = manager.dialog_data
    if data["mod_value"] < 11:
        data["mod_value"] += 1
    else:
        data["mod_value"] = 0


async def down_key(c: CallbackQuery, widget: Any, manager: DialogManager):
    await c.answer()
    data = manager.dialog_data
    if data["mod_value"] > -11:
        data["mod_value"] -= 1
    else:
        data["mod_value"] = 0


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
