from aiogram import Router

# from .dialogs import songs, favorite_songs
from .dialogs import favorite_songs, all_songs


def setup(router: Router):
    # router.include_router(songs)
    router.include_router(favorite_songs)
    router.include_router(all_songs)
