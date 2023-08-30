from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start, Cancel, Select, SwitchTo, Button, ScrollingGroup
from aiogram_dialog.widgets.text import Jinja, Const, Format

from .getters import (
    get_song,
    get_all_songs,
    get_chords,
    get_songs_by_band,
    get_favorite_songs,
)
from .handlers import (
    select_song,
    select_song_by_band,
    select_favorite_song,
)
from src.tgbot import states
from ..preview_data import PREVIEW_SONG


all_songs = Dialog(
    Window(
        Const("Все песни"),
        ScrollingGroup(
            Select(
                Format("{item.title}"),
                id="all_songs",
                item_id_getter=lambda x: x.id,
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
            "Выбрана песня {{ song.title }} группы {{ song.band.title }}"
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
        # Hardcode jinja but whatever
        Jinja(
            "Аккорды для песни \n"
            "{% for verse_string in verses_strings %}"
            "{% for chord in verse_string.chords %}"
            "{% if verse_string.chords_count == 1 %}"
            "{{ chord.title }}"
            "{% elif verse_string.chords_count == 2 %}"
            "{{ '%-40s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 3 %}"
            "{{ '%-26s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 4 %}"
            "{{ '%-17s'|format(chord.title) }}"
            "{% endif %}"
            "{% endfor %}"
            "\n\n{{ verse_string.lyrics }}\n"
            "{% endfor %}"
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


songs_by_group = Dialog(
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


favorite_songs = Dialog(
    Window(
        Const("Избранные песни"),
        ScrollingGroup(
            Select(
                Format("{item[title]}"),
                id="favorite_songs",
                item_id_getter=lambda x: x['id'],
                items="songs",
                on_click=select_favorite_song,
            ),
            id="favorite_songs_sg",
            width=1,
            height=10,
        ),
        Cancel(Const("[Emodji]Назад")),
        state=states.FavoriteSongsPanelSG.choose_song,
        preview_data={"songs": [PREVIEW_SONG]},
        getter=get_favorite_songs,
    ),
    Window(
        Jinja(
            "Выбрана песня {{ title }} группы {{ band }}"
        ),
        SwitchTo(
            Const("[Emodji]Аккорды"),
            id="to_chords",
            state=states.FavoriteSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("[Emodji]Назад к избраным песням"),
            id="to_band",
            state=states.FavoriteSongsPanelSG.choose_song,
        ),
        state=states.FavoriteSongsPanelSG.song_menu,
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
            state=states.FavoriteSongsPanelSG.song_menu,
        ),
        state=states.FavoriteSongsPanelSG.song_chords,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords,
    ),
)
