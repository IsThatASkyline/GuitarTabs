from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    ScrollingGroup,
    Select,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Jinja

from guitar_app.presentation.tgbot import states
from guitar_app.presentation.tgbot.dialogs.song_manage.founded_songs.getters import (
    get_songs_founded_by_title,
)
from guitar_app.presentation.tgbot.dialogs.song_manage.founded_songs.handlers import (
    find_song_by_title,
    select_founded_song_tab,
    select_song_founded_by_title,
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

songs_founded_by_title = Dialog(
    Window(
        Jinja("🔍Введите название песни"),
        MessageInput(func=find_song_by_title),
        Start(Const("🔙Назад"), id="back", state=states.MainMenuSG.main),
        state=states.FoundedSongsPanelSG.input_song_title,
    ),
    Window(
        Jinja(
            "{% if songs %}"
            "Песни с названием: <b>{{ song_title }}</b> (Всего: <b>{{ songs|length }}</b>)"
            "{% else %}"
            "Песен с названием <b>{{ song_title }}</b> не найдено"
            "{% endif %}"
        ),
        ScrollingGroup(
            Select(
                Format("{item.title}"),
                id="founded_songs",
                item_id_getter=lambda x: x.id,
                items="songs",
                on_click=select_song_founded_by_title,
            ),
            id="founded_songs_sg",
            width=1,
            height=7,
            when=F["songs"],
        ),
        Cancel(Const("🔙Назад")),
        state=states.FoundedSongsPanelSG.choose_song,
        getter=get_songs_founded_by_title,
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
            Const("📖 Текст и аккорды"),
            id="to_chords",
            state=states.FoundedSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("🔙Назад к найденным песням"),
            id="to_all_songs",
            state=states.FoundedSongsPanelSG.choose_song,
        ),
        state=states.FoundedSongsPanelSG.song_menu,
        getter=get_song,
    ),
    Window(
        templates.SONG_CHORDS_WITHOUT_TABS_TEMPLATE,
        SwitchTo(
            Const("🎼Показать табы"),
            id="to_tabs",
            state=states.FoundedSongsPanelSG.song_tabs,
            when=F["song"].tabs,
        ),
        menu.modulation_menu,
        SwitchTo(
            Const("📜Показать аппликатуры аккордов"),
            id="to_chords_tabs",
            state=states.FoundedSongsPanelSG.song_chords_with_tabs,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.FoundedSongsPanelSG.song_menu,
            on_click=refresh_mod_value,
        ),
        state=states.FoundedSongsPanelSG.song_chords,
        getter=get_chords,
    ),
    Window(
        templates.SONG_CHORDS_WITH_TABS_TEMPLATE,
        SwitchTo(
            Const("🎼Показать табы"),
            id="to_tabs",
            state=states.FoundedSongsPanelSG.song_tabs,
            when=F["song"].tabs,
        ),
        menu.modulation_menu,
        SwitchTo(
            Const("📜Показать текст и аккорды"),
            id="to_chords",
            state=states.FoundedSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.FoundedSongsPanelSG.song_menu,
            on_click=refresh_mod_value,
        ),
        state=states.FoundedSongsPanelSG.song_chords_with_tabs,
        getter=get_chords,
    ),
    Window(
        Jinja("Табы к <b>{{ band_title }} - {{ song_title }}</b>"),
        ScrollingGroup(
            Select(
                Format("{item.title}"),
                id="founded_song_tabs",
                item_id_getter=lambda x: x.id,
                items="tabs",
                on_click=select_founded_song_tab,
            ),
            id="founded_songs_tabs_sg",
            width=1,
            height=7,
            when=F["tabs"],
        ),
        SwitchTo(
            Const("🔙Назад к аккордам"),
            id="to_song",
            state=states.FoundedSongsPanelSG.song_chords,
            on_click=refresh_mod_value,
        ),
        state=states.FoundedSongsPanelSG.song_tabs,
        getter=get_all_tabs,
    ),
    Window(
        Format("{title}"),
        DynamicMedia("tab"),
        SwitchTo(
            Const("🔙Назад ко всем табам"),
            id="to_tabs",
            state=states.FoundedSongsPanelSG.song_tabs,
        ),
        state=states.FoundedSongsPanelSG.song_tab_detail,
        getter=get_detail_tab,
    ),
    Window(
        Const("Введите текстовое название"),
        Cancel(Const("🔙Назад")),
        state=states.FoundedSongsPanelSG.message_type_error,
    ),
)
