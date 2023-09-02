from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Cancel, Select, SwitchTo, Button, ScrollingGroup
from aiogram_dialog.widgets.text import Jinja, Const, Format

from .getters import (
    get_song,
    get_all_songs,
    get_chords,
    get_songs_by_band,
    get_favorite_songs, get_songs_founded_by_title,
)
from .handlers import (
    select_song,
    select_song_by_band,
    select_favorite_song,
    add_song_to_favorite,
    remove_song_from_favorite, find_song_by_title, select_song_founded_by_title,
)
from src.tgbot import states
from ..preview_data import PREVIEW_SONG

am = """
        E | A | D | G | H | e
       --＋--＋--＋--＋--＋--
        – | – | – | – | O | – 1
        – | – | O | O | – | – 2
        – | – | – | – | – | – 3
     """

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
            height=7,
        ),
        Cancel(Const("[Emodji]Назад")),
        state=states.AllSongsPanelSG.choose_song,
        preview_data={"songs": [PREVIEW_SONG]},
        getter=get_all_songs,
    ),
    Window(
        Jinja(
            "Выбрана песня {{ song.title }} группы {{ song.band.title }}\n"
            "Аккорды в песне:\n"
            f"Am: {am}"
        ),
        Button(
            Const("[Emodji]Добавить в избранное"),
            id="add_to_favorite",
            on_click=add_song_to_favorite,
            when=~F["in_favorites"],
        ),
        Button(
            Const("[Emodji]Убрать из избранного"),
            id="remove_from_favorite",
            on_click=remove_song_from_favorite,
            when=F["in_favorites"],
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
            "{% for verse in verses %}"
            "\n\n{{ verse.title }}:\n"
            "{% for verse_string in verse.strings%}"
            "{% for chord in verse_string.chords %}"
            "{% if verse_string.chords_count == 1 %}"
            "{{ chord.title }}"
            "{% elif verse_string.chords_count == 2 %}"
            "{{ '%-50s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 3 %}"
            "{{ '%-26s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 4 %}"
            "{{ '%-17s'|format(chord.title) }}"
            "{% endif %}"
            "{% endfor %}"
            "\n\n{{ verse_string.lyrics }}\n"
            "{% endfor %}"
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
                Format("{item.title}"),
                id="songs_by_band",
                item_id_getter=lambda x: x.id,
                items="songs",
                on_click=select_song_by_band,
            ),
            id="songs_by_band_sg",
            width=1,
            height=7,
        ),
        Cancel(Const("[Emodji]Назад")),
        state=states.BandSongsPanelSG.choose_song,
        getter=get_songs_by_band,
    ),
    Window(
        Jinja(
            "Выбрана песня {{ song.title }} группы {{ song.band.title }}"
        ),
        Button(
            Const("[Emodji]Добавить в избранное"),
            id="add_to_favorite",
            on_click=add_song_to_favorite,
            when=~F["in_favorites"],
        ),
        Button(
            Const("[Emodji]Убрать из избранного"),
            id="remove_from_favorite",
            on_click=remove_song_from_favorite,
            when=F["in_favorites"],
        ),
        SwitchTo(
            Const("[Emodji]Аккорды"),
            id="to_chords",
            state=states.BandSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("[Emodji]Назад к песням группы"),
            id="to_all_songs",
            state=states.BandSongsPanelSG.choose_song,
        ),
        state=states.BandSongsPanelSG.song_menu,
        preview_data={"song": PREVIEW_SONG},
        getter=get_song,
    ),
    Window(
        # Hardcode jinja but whatever
        Jinja(
            "Аккорды для песни \n"
            "{% for verse in verses %}"
            "\n\n{{ verse.title }}:\n"
            "{% for verse_string in verse.strings%}"
            "{% for chord in verse_string.chords %}"
            "{% if verse_string.chords_count == 1 %}"
            "{{ chord.title }}"
            "{% elif verse_string.chords_count == 2 %}"
            "{{ '%-50s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 3 %}"
            "{{ '%-26s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 4 %}"
            "{{ '%-17s'|format(chord.title) }}"
            "{% endif %}"
            "{% endfor %}"
            "\n\n{{ verse_string.lyrics }}\n"
            "{% endfor %}"
            "{% endfor %}"
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
                Format("{item.title}"),
                id="favorite_songs",
                item_id_getter=lambda x: x.id,
                items="songs",
                on_click=select_favorite_song,
            ),
            id="favorite_songs_sg",
            width=1,
            height=7,
        ),
        Cancel(Const("[Emodji]Назад")),
        state=states.FavoriteSongsPanelSG.choose_song,
        preview_data={"songs": [PREVIEW_SONG]},
        getter=get_favorite_songs,
    ),
    Window(
        Jinja(
            "Выбрана песня {{ song.title }} группы {{ song.band.title }}"
        ),
        Button(
            Const("[Emodji]Добавить в избранное"),
            id="add_to_favorite",
            on_click=add_song_to_favorite,
            when=~F["in_favorites"],
        ),
        Button(
            Const("[Emodji]Убрать из избранного"),
            id="remove_from_favorite",
            on_click=remove_song_from_favorite,
            when=F["in_favorites"],
        ),
        SwitchTo(
            Const("[Emodji]Аккорды"),
            id="to_chords",
            state=states.FavoriteSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("[Emodji]Назад к избранным песням"),
            id="to_all_songs",
            state=states.FavoriteSongsPanelSG.choose_song,
        ),
        state=states.FavoriteSongsPanelSG.song_menu,
        preview_data={"song": PREVIEW_SONG},
        getter=get_song,
    ),
    Window(
        # Hardcode jinja but whatever
        Jinja(
            "Аккорды для песни \n"
            "{% for verse in verses %}"
            "\n\n{{ verse.title }}:\n"
            "{% for verse_string in verse.strings%}"
            "{% for chord in verse_string.chords %}"
            "{% if verse_string.chords_count == 1 %}"
            "{{ chord.title }}"
            "{% elif verse_string.chords_count == 2 %}"
            "{{ '%-50s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 3 %}"
            "{{ '%-26s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 4 %}"
            "{{ '%-17s'|format(chord.title) }}"
            "{% endif %}"
            "{% endfor %}"
            "\n\n{{ verse_string.lyrics }}\n"
            "{% endfor %}"
            "{% endfor %}"
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


songs_founded_by_title = Dialog(
    Window(
        Jinja("Введите название песни"),
        MessageInput(func=find_song_by_title),
        Start(Const("🔙Назад"), id="back", state=states.MainMenuSG.main),
        state=states.FoundedSongsPanelSG.input_song_title,
    ),
    Window(
        Jinja("Найденные песни по названию: {{ song_title }}"),
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
        ),
        Cancel(Const("[Emodji]Назад")),
        state=states.FoundedSongsPanelSG.choose_song,
        preview_data={"songs": [PREVIEW_SONG]},
        getter=get_songs_founded_by_title,
    ),
    Window(
        Jinja(
            "Выбрана песня {{ song.title }} группы {{ song.band.title }}"
        ),
        Button(
            Const("[Emodji]Добавить в избранное"),
            id="add_to_favorite",
            on_click=add_song_to_favorite,
            when=~F["in_favorites"],
        ),
        Button(
            Const("[Emodji]Убрать из избранного"),
            id="remove_from_favorite",
            on_click=remove_song_from_favorite,
            when=F["in_favorites"],
        ),
        SwitchTo(
            Const("[Emodji]Аккорды"),
            id="to_chords",
            state=states.FoundedSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("[Emodji]Назад к найденным песням"),
            id="to_all_songs",
            state=states.FoundedSongsPanelSG.choose_song,
        ),
        state=states.FoundedSongsPanelSG.song_menu,
        preview_data={"song": PREVIEW_SONG},
        getter=get_song,
    ),
    Window(
        # Hardcode jinja but whatever
        Jinja(
            "Аккорды для песни \n"
            "{% for verse in verses %}"
            "\n\n{{ verse.title }}:\n"
            "{% for verse_string in verse.strings%}"
            "{% for chord in verse_string.chords %}"
            "{% if verse_string.chords_count == 1 %}"
            "{{ chord.title }}"
            "{% elif verse_string.chords_count == 2 %}"
            "{{ '%-50s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 3 %}"
            "{{ '%-26s'|format(chord.title) }}"
            "{% elif verse_string.chords_count == 4 %}"
            "{{ '%-17s'|format(chord.title) }}"
            "{% endif %}"
            "{% endfor %}"
            "\n\n{{ verse_string.lyrics }}\n"
            "{% endfor %}"
            "{% endfor %}"
        ),
        SwitchTo(
            Const("[Emodji]Назад к меню песни"),
            id="to_song",
            state=states.FoundedSongsPanelSG.song_menu,
        ),
        state=states.FoundedSongsPanelSG.song_chords,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords,
    ),
)
