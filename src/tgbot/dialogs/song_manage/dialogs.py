from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Cancel, Select, SwitchTo, Button, ScrollingGroup
from aiogram_dialog.widgets.text import Jinja, Const, Format

from .getters import (
    # get_search_history_songs,
    get_song,
    get_favorite_songs,
    get_all_songs,
    get_chords,
)
from .handlers import (
    select_song,
    remove_song_from_favorites,
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
                id="songs",
                item_id_getter=lambda x: x['id'],
                items="songs",
                on_click=select_song,
            ),
            id="songs_sg",
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
            Const("[Emodji]Назад к списку песен"),
            id="to_songs",
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
            Const("[Emodji]Назад к списку песен"),
            id="to_songs",
            state=states.AllSongsPanelSG.choose_song,
        ),
        state=states.AllSongsPanelSG.song_chords,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords,
    ),
)


favorite_songs = Dialog(
    Window(
        Const("Избранные песни"),
        ScrollingGroup(
            Select(
                Format("{item[title]}"),
                id="songs",
                item_id_getter=lambda x: x['id'],
                items="songs",
                on_click=select_song,
            ),
            id="songs_sg",
            width=1,
            height=10,
        ),
        Cancel(Const("[Emodji]Назад")),
        state=states.FavoriteSongsPanelSG.list,
        preview_data={"songs": [PREVIEW_SONG]},
        getter=get_favorite_songs,
    ),
    Window(
        Jinja(
            "Выбрана песня <b>{{ title }}</b> группы {{ band }}"
        ),
        SwitchTo(
            Const("[Emodji]Аккорды"),
            id="to_chords",
            state=states.SongPanelSG.chords,
        ),
        SwitchTo(
            Const("[Emodji]Группа"),
            id="to_band",
            state=states.SongPanelSG.band,
        ),
        Button(
            Const("[Emodji]Удалить из избранных"),
            id="remove_song_from_favorites",
            on_click=remove_song_from_favorites,
            when=F['song'].can_be_removed_from_favorites,
        ),
        SwitchTo(
            Const("[Emodji]Назад к списку песен"),
            id="to_songs",
            state=states.FavoriteSongsPanelSG.list,
        ),
        state=states.FavoriteSongsPanelSG.choose_song,
        preview_data={"song": PREVIEW_SONG},
        getter=get_song,
    ),
)

