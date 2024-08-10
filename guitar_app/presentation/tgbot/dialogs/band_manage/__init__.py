from aiogram import Router

from .dialogs import all_bands


def setup(router: Router):
    router.include_router(all_bands)
