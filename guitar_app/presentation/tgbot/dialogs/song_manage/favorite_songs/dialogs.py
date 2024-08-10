from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, ScrollingGroup, Select, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Jinja

from guitar_app.presentation.tgbot import states
from guitar_app.presentation.tgbot.dialogs.song_manage.favorite_songs.getters import (
    get_favorite_songs,
)
from guitar_app.presentation.tgbot.dialogs.song_manage.favorite_songs.handlers import (
    select_favorite_song,
    select_favorite_song_tab,
)
from guitar_app.presentation.tgbot.dialogs.song_manage.getters import (
    get_all_tabs,
    get_chords,
    get_detail_tab,
    get_song,
)
from guitar_app.presentation.tgbot.dialogs.song_manage.handlers import (
    add_song_to_favorite,
    refresh_mod_value,
    remove_song_from_favorite,
)
from guitar_app.presentation.tgbot.jinja.templates import menu, templates

favorite_songs = Dialog(
    Window(
        Const("⭐️Избранные песни"),
        ScrollingGroup(
            Select(
                Format("{item.title}"),
                id="favorite_songs",
                item_id_getter=lambda x: x.id,
                items="songs",
                on_click=select_favorite_song,
            ),
            id="favorite_songs_sg",
            width=1,
            height=7,
            when=F["songs"],
        ),
        Cancel(Const("🔙Назад")),
        state=states.FavoriteSongsPanelSG.choose_song,
        getter=get_favorite_songs,
    ),
    Window(
        templates.SONG_MENU,
        Button(
            Const("⭐️Добавить в избранное"),
            id="add_to_favorite",
            on_click=add_song_to_favorite,
            when=~F["in_favorites"],
        ),
        Button(
            Const("🗑Убрать из избранного"),
            id="remove_from_favorite",
            on_click=remove_song_from_favorite,
            when=F["in_favorites"],
        ),
        SwitchTo(
            Const("📖Текст и аккорды"),
            id="to_chords",
            state=states.FavoriteSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("🔙Назад к избранным песням"),
            id="to_all_songs",
            state=states.FavoriteSongsPanelSG.choose_song,
        ),
        state=states.FavoriteSongsPanelSG.song_menu,
        getter=get_song,
    ),
    Window(
        templates.SONG_CHORDS_WITHOUT_TABS_TEMPLATE,
        SwitchTo(
            Const("🎼Показать табы"),
            id="to_tabs",
            state=states.FavoriteSongsPanelSG.song_tabs,
            when=F["song"].tabs,
        ),
        menu.modulation_menu,
        SwitchTo(
            Const("📜Показать аппликатуры аккордов"),
            id="to_chords_tabs",
            state=states.FavoriteSongsPanelSG.song_chords_with_tabs,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.FavoriteSongsPanelSG.song_menu,
            on_click=refresh_mod_value,
        ),
        state=states.FavoriteSongsPanelSG.song_chords,
        getter=get_chords,
    ),
    Window(
        templates.SONG_CHORDS_WITH_TABS_TEMPLATE,
        SwitchTo(
            Const("🎼Показать табы"),
            id="to_tabs",
            state=states.FavoriteSongsPanelSG.song_tabs,
            when=F["song"].tabs,
        ),
        menu.modulation_menu,
        SwitchTo(
            Const("📜Показать текст и аккорды"),
            id="to_chords",
            state=states.FavoriteSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.FavoriteSongsPanelSG.song_menu,
            on_click=refresh_mod_value,
        ),
        state=states.FavoriteSongsPanelSG.song_chords_with_tabs,
        getter=get_chords,
    ),
    Window(
        Jinja("Табы к <b>{{ band_title }} - {{ song_title }}</b>"),
        ScrollingGroup(
            Select(
                Format("{item.title}"),
                id="favorite_song_tabs",
                item_id_getter=lambda x: x.id,
                items="tabs",
                on_click=select_favorite_song_tab,
            ),
            id="favorite_songs_tabs_sg",
            width=1,
            height=7,
            when=F["tabs"],
        ),
        SwitchTo(
            Const("🔙Назад к аккордам"),
            id="to_song",
            state=states.FavoriteSongsPanelSG.song_chords,
            on_click=refresh_mod_value,
        ),
        state=states.FavoriteSongsPanelSG.song_tabs,
        getter=get_all_tabs,
    ),
    Window(
        Format("{title}"),
        DynamicMedia("tab"),
        SwitchTo(
            Const("🔙Назад ко всем табам"),
            id="to_tabs",
            state=states.FavoriteSongsPanelSG.song_tabs,
        ),
        state=states.FavoriteSongsPanelSG.song_tab_detail,
        getter=get_detail_tab,
    ),
)
