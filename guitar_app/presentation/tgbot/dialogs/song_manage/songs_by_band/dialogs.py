from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    ScrollingGroup,
    Select,
    SwitchTo,
)
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Jinja

from guitar_app.presentation.tgbot import states
from guitar_app.presentation.tgbot.dialogs.song_manage.getters import get_song, get_chords, get_all_tabs, get_detail_tab
from guitar_app.presentation.tgbot.dialogs.song_manage.handlers import add_song_to_favorite, remove_song_from_favorite, \
    refresh_mod_value
from guitar_app.presentation.tgbot.dialogs.song_manage.songs_by_band.getters import get_songs_by_band
from guitar_app.presentation.tgbot.dialogs.song_manage.songs_by_band.handlers import select_song_by_band, \
    select_band_song_tab
from guitar_app.presentation.tgbot.jinja.templates import templates, menu

songs_by_band = Dialog(
    Window(
        Jinja("🎵Песни группы <b>{{ band_title }}</b> (Всего: <b>{{ songs|length }}</b>)"),
        ScrollingGroup(
            Select(
                Format("{item.title}"),
                id="songs_by_band",
                item_id_getter=lambda x: x.id,
                items="songs",
                on_click=select_song_by_band,
                when=F["songs"],
            ),
            id="songs_by_band_sg",
            width=2,
            height=7,
        ),
        Cancel(Const("🔙Назад")),
        state=states.BandSongsPanelSG.choose_song,
        getter=get_songs_by_band,
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
            state=states.BandSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("🔙Назад к песням группы"),
            id="to_all_songs",
            state=states.BandSongsPanelSG.choose_song,
        ),
        state=states.BandSongsPanelSG.song_menu,
        getter=get_song,
    ),
    Window(
        templates.SONG_CHORDS_WITHOUT_TABS_TEMPLATE,
        SwitchTo(
            Const("🎼Показать табы"),
            id="to_tabs",
            state=states.BandSongsPanelSG.song_tabs,
            when=F["song"].tabs,
        ),
        menu.modulation_menu,
        SwitchTo(
            Const("📜Показать аппликатуры аккордов"),
            id="to_chords_tabs",
            state=states.BandSongsPanelSG.song_chords_with_tabs,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.BandSongsPanelSG.song_menu,
            on_click=refresh_mod_value,
        ),
        state=states.BandSongsPanelSG.song_chords,
        getter=get_chords,
    ),
    Window(
        templates.SONG_CHORDS_WITH_TABS_TEMPLATE,
        SwitchTo(
            Const("🎼Показать табы"),
            id="to_tabs",
            state=states.BandSongsPanelSG.song_tabs,
            when=F["song"].tabs,
        ),
        menu.modulation_menu,
        SwitchTo(
            Const("📜Показать текст и аккорды"),
            id="to_chords",
            state=states.BandSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.BandSongsPanelSG.song_menu,
            on_click=refresh_mod_value,
        ),
        state=states.BandSongsPanelSG.song_chords_with_tabs,
        getter=get_chords,
    ),
    Window(
        Jinja("Табы к <b>{{ band_title }} - {{ song_title }}</b>"),
        ScrollingGroup(
            Select(
                Format("{item.title}"),
                id="band_song_tabs",
                item_id_getter=lambda x: x.id,
                items="tabs",
                on_click=select_band_song_tab,
            ),
            id="band_songs_tabs_sg",
            width=1,
            height=7,
            when=F["tabs"],
        ),
        SwitchTo(
            Const("🔙Назад к аккордам"),
            id="to_song",
            state=states.BandSongsPanelSG.song_chords,
            on_click=refresh_mod_value,
        ),
        state=states.BandSongsPanelSG.song_tabs,
        getter=get_all_tabs,
    ),
    Window(
        Format("{title}"),
        DynamicMedia("tab"),
        SwitchTo(
            Const("🔙Назад ко всем табам"),
            id="to_tabs",
            state=states.BandSongsPanelSG.song_tabs,
        ),
        state=states.BandSongsPanelSG.song_tab_detail,
        getter=get_detail_tab,
    ),
)
