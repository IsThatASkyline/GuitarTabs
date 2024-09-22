from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, Start, SwitchTo
from aiogram_dialog.widgets.text import Const, Jinja

from guitar_app.presentation.tgbot import states
from guitar_app.presentation.tgbot.dialogs.main_menu.getters import get_main
from guitar_app.presentation.tgbot.jinja.templates import templates

main_menu = Dialog(
    Window(
        Jinja("Привет, Гитарист!\n" "Ты находишься в главном меню.\n"),
        Start(
            Const("⭐️Избранные песни"),
            id="favorite_songs",
            state=states.FavoriteSongsPanelSG.choose_song,
        ),
        Start(
            Const("🎵Все песни"),
            id="all_songs",
            state=states.AllSongsPanelSG.choose_song,
        ),
        Start(
            Const("🎸Все группы"),
            id="all_bands",
            state=states.AllBandsPanelSG.choose_band,
        ),
        Start(
            Const("🔍Найти песню по названию"),
            id="find_songs",
            state=states.FoundedSongsPanelSG.input_song_title,
        ),
        SwitchTo(
            Const("📌О боте"),
            id="about",
            state=states.MainMenuSG.about,
        ),
        state=states.MainMenuSG.main,
        getter=get_main,
    ),
    Window(
        templates.ABOUT,
        SwitchTo(
            Const("🔙Назад"),
            id="to_main_menu",
            state=states.MainMenuSG.main,
        ),
        state=states.MainMenuSG.about,
    ),
)
