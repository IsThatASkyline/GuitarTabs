from aiogram import Router

from .dialogs import all_songs, all_songs_by_group


def setup(router: Router):
    router.include_router(all_songs)
    router.include_router(all_songs_by_group)
