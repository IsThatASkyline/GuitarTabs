from aiogram import Router

from .dialogs import (
    all_songs,
    songs_by_group,
    favorite_songs,
    songs_founded_by_title,
)


def setup(router: Router):
    router.include_router(all_songs)
    router.include_router(songs_by_group)
    router.include_router(favorite_songs)
    router.include_router(songs_founded_by_title)
