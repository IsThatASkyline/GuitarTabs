from aiogram import Router

from .all_songs import all_songs
from .favorite_songs import favorite_songs
from .songs_by_band import songs_by_band
from .founded_songs import songs_founded_by_title


def setup(router: Router):
    router.include_router(all_songs)
    router.include_router(songs_by_band)
    router.include_router(favorite_songs)
    router.include_router(songs_founded_by_title)
