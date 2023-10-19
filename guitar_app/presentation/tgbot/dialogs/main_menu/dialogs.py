from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, Start
from aiogram_dialog.widgets.text import Const, Jinja

from guitar_app.presentation.tgbot import states
from guitar_app.presentation.tgbot.dialogs.main_menu.getters import get_main

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
        Cancel(Const("🚪Закрыть")),
        state=states.MainMenuSG.main,
        getter=get_main,
    ),
)
