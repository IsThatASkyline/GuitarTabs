from aiogram import Router

from .dialogs import main_menu


def setup(router: Router):
    router.include_router(main_menu)