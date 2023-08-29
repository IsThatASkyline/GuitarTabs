from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Cancel, Select, SwitchTo, Button, ScrollingGroup
from aiogram_dialog.widgets.text import Jinja, Const, Format

from .getters import (
    get_song,
    get_all_songs,
    get_chords, get_songs_by_band,
)
from .handlers import (
    select_song,
    select_song_by_band,
    show_chords,
)
from src.tgbot import states
from ..preview_data import PREVIEW_SONG


all_songs = Dialog(
    Window(
        Const("Все песни"),
        ScrollingGroup(
            Select(
                Format("{item[title]}"),
                id="all_songs",
                item_id_getter=lambda x: x['id'],
                items="songs",
                on_click=select_song,
            ),
            id="all_songs_sg",
            width=1,
            height=10,
        ),
        Cancel(Const("[Emodji]Назад")),
        state=states.AllSongsPanelSG.choose_song,
        preview_data={"songs": [PREVIEW_SONG]},
        getter=get_all_songs,
    ),
    Window(
        Jinja(
            "Выбрана песня {{ title }} группы {{ band }}"
        ),
        SwitchTo(
            Const("[Emodji]Аккорды"),
            id="to_chords",
            state=states.AllSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("[Emodji]Назад ко всем песням"),
            id="to_all_songs",
            state=states.AllSongsPanelSG.choose_song,
        ),
        state=states.AllSongsPanelSG.song_menu,
        preview_data={"song": PREVIEW_SONG},
        getter=get_song,
    ),
    Window(
        Jinja(
            "Аккорды для песни {{title}}\n"
            "{{chords}}\n"
            "{{chords}}\n"
            "{{chords}}\n"
            "{{chords}}\n"
            "{{chords}}\n"
        ),
        SwitchTo(
            Const("[Emodji]Назад к меню песни"),
            id="to_song",
            state=states.AllSongsPanelSG.song_menu,
        ),
        state=states.AllSongsPanelSG.song_chords,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords,
    ),
)


all_songs_by_group = Dialog(
    Window(
        Const("Все песни определенной группы"),
        ScrollingGroup(
            Select(
                Format("{item[title]}"),
                id="songs_by_band",
                item_id_getter=lambda x: x['id'],
                items="songs",
                on_click=select_song_by_band,
            ),
            id="songs_by_band_sg",
            width=1,
            height=10,
        ),
        Cancel(Const("[Emodji]Назад")),
        state=states.BandSongsPanelSG.choose_song,
        preview_data={"songs": [PREVIEW_SONG]},
        getter=get_songs_by_band,
    ),
    Window(
        Jinja(
            "Выбрана песня {{ title }} группы {{ band }}"
        ),
        SwitchTo(
            Const("[Emodji]Аккорды"),
            id="to_chords",
            state=states.BandSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("[Emodji]Назад к песням группы"),
            id="to_band",
            state=states.BandSongsPanelSG.choose_song,
        ),
        state=states.BandSongsPanelSG.song_menu,
        preview_data={"song": PREVIEW_SONG},
        getter=get_song,
    ),
    Window(
        Jinja(
            "Аккорды для песни {{title}}\n"
            "{{chords}}\n"
            "{{chords}}\n"
            "{{chords}}\n"
            "{{chords}}\n"
            "{{chords}}\n"
        ),
        SwitchTo(
            Const("[Emodji]Назад к меню песни"),
            id="to_song",
            state=states.BandSongsPanelSG.song_menu,
        ),
        state=states.BandSongsPanelSG.song_chords,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords,
    ),
)
