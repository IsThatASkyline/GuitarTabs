from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Cancel, Select, SwitchTo, Button, ScrollingGroup
from aiogram_dialog.widgets.text import Jinja, Const, Format

from .getters import (
    get_song,
    get_band,
    get_all_bands,
    get_songs_by_band,
)
from .handlers import (
    select_band,
    select_song,
)
from src.tgbot import states
from ..preview_data import PREVIEW_SONG


all_bands = Dialog(
    Window(
        Const("Все группы"),
        ScrollingGroup(
            Select(
                Format("{item[title]}"),
                id="bands",
                item_id_getter=lambda x: x['id'],
                items="bands",
                on_click=select_band,
            ),
            id="bands_sg",
            width=1,
            height=10,
        ),
        Cancel(Const("[Emodji]Назад")),
        state=states.AllBandsPanelSG.choose_band,
        getter=get_all_bands,
    ),
    Window(
        Const("Определенная группа"),
        ScrollingGroup(
            Select(
                Format("{item[title]}"),
                id="songs_by_group",
                item_id_getter=lambda x: x['id'],
                items="songs",
                on_click=select_song,
            ),
            id="bands_sg",
            width=1,
            height=10,
        ),
        SwitchTo(
            Const("[Emodji]Назад к списку групп"),
            id="to_bands",
            state=states.AllBandsPanelSG.choose_band,
        ),
        state=states.AllBandsPanelSG.band_songs,
        getter=get_songs_by_band,
    ),
    Window(
        Jinja(
            "Выбрана песня {{ title }} группы {{ band }}"
        ),
        SwitchTo(
            Const("[Emodji]Аккорды"),
            id="to_chords",
            state=states.AllBandsPanelSG.band_song_chords,
        ),
        SwitchTo(
            Const("[Emodji]Назад к списку песен"),
            id="to_songs",
            state=states.AllBandsPanelSG.band_songs,
        ),
        Cancel(Const("[Emodji]Назад")),
        state=states.AllBandsPanelSG.band_song,
        preview_data={"song": PREVIEW_SONG},
        getter=get_song,
    ),
)
