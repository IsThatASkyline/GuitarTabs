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
from aiogram_dialog.widgets.text import Const, Format, Jinja

from ... import states
from ...jinja.templates import templates
from ..preview_data import PREVIEW_SONG
from .getters import (
    get_all_songs,
    get_chords,
    get_chords_with_tabs,
    get_favorite_songs,
    get_song,
    get_songs_by_band,
    get_songs_founded_by_title,
)
from .handlers import (
    add_song_to_favorite,
    find_song_by_title,
    remove_song_from_favorite,
    select_favorite_song,
    select_song,
    select_song_by_band,
    select_song_founded_by_title,
)


all_songs = Dialog(
    Window(
        Const("🎵Все песни"),
        ScrollingGroup(
            Select(
                Format("{item.title}"),
                id="all_songs",
                item_id_getter=lambda x: x.id,
                items="songs",
                on_click=select_song,
            ),
            id="all_songs_sg",
            width=2,
            height=7,
            when=F["songs"],
        ),
        Cancel(Const("🔙Назад")),
        state=states.AllSongsPanelSG.choose_song,
        preview_data={"songs": [PREVIEW_SONG]},
        getter=get_all_songs,
    ),
    Window(
        Jinja("<b>{{ song.title }}</b> группы <b>{{ song.band.title }}</b>"),
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
            state=states.AllSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("🔙Назад ко всем песням"),
            id="to_all_songs",
            state=states.AllSongsPanelSG.choose_song,
        ),
        state=states.AllSongsPanelSG.song_menu,
        preview_data={"song": PREVIEW_SONG},
        getter=get_song,
    ),
    Window(
        templates.SONG_CHORDS_WITHOUT_TABS_TEMPLATE,
        SwitchTo(
            Const("📜Показать аппликатуры аккордов"),
            id="to_chords_tabs",
            state=states.AllSongsPanelSG.song_chords_with_tabs,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.AllSongsPanelSG.song_menu,
        ),
        state=states.AllSongsPanelSG.song_chords,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords,
    ),
    Window(
        templates.SONG_CHORDS_WITH_TABS_TEMPLATE,
        SwitchTo(
            Const("📜Убрать аппликатуры аккордов"),
            id="to_chords",
            state=states.AllSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.AllSongsPanelSG.song_menu,
        ),
        state=states.AllSongsPanelSG.song_chords_with_tabs,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords_with_tabs,
    ),
)


songs_by_group = Dialog(
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
            width=1,
            height=7,
        ),
        Cancel(Const("🔙Назад")),
        state=states.BandSongsPanelSG.choose_song,
        getter=get_songs_by_band,
    ),
    Window(
        Jinja("<b>{{ song.title }}</b> группы <b>{{ song.band.title }}</b>"),
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
        preview_data={"song": PREVIEW_SONG},
        getter=get_song,
    ),
    Window(
        templates.SONG_CHORDS_WITHOUT_TABS_TEMPLATE,
        SwitchTo(
            Const("📜Показать аппликатуры аккордов"),
            id="to_chords_tabs",
            state=states.BandSongsPanelSG.song_chords_with_tabs,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.BandSongsPanelSG.song_menu,
        ),
        state=states.BandSongsPanelSG.song_chords,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords,
    ),
    Window(
        templates.SONG_CHORDS_WITH_TABS_TEMPLATE,
        SwitchTo(
            Const("📜Убрать аппликатуры аккордов"),
            id="to_chords",
            state=states.BandSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.BandSongsPanelSG.song_menu,
        ),
        state=states.BandSongsPanelSG.song_chords_with_tabs,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords_with_tabs,
    ),
)


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
        preview_data={"songs": [PREVIEW_SONG]},
        getter=get_favorite_songs,
    ),
    Window(
        Jinja("<b>{{ song.title }}</b> группы <b>{{ song.band.title }}</b>"),
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
        preview_data={"song": PREVIEW_SONG},
        getter=get_song,
    ),
    Window(
        templates.SONG_CHORDS_WITHOUT_TABS_TEMPLATE,
        SwitchTo(
            Const("📜Показать аппликатуры аккордов"),
            id="to_chords_tabs",
            state=states.FavoriteSongsPanelSG.song_chords_with_tabs,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.FavoriteSongsPanelSG.song_menu,
        ),
        state=states.FavoriteSongsPanelSG.song_chords,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords,
    ),
    Window(
        templates.SONG_CHORDS_WITH_TABS_TEMPLATE,
        SwitchTo(
            Const("📜Убрать аппликатуры аккордов"),
            id="to_chords",
            state=states.FavoriteSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.FavoriteSongsPanelSG.song_menu,
        ),
        state=states.FavoriteSongsPanelSG.song_chords_with_tabs,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords_with_tabs,
    ),
)


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
        Jinja("<b>{{ song.title }}</b> группы <b>{{ song.band.title }}</b>"),
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
        preview_data={"song": PREVIEW_SONG},
        getter=get_song,
    ),
    Window(
        templates.SONG_CHORDS_WITHOUT_TABS_TEMPLATE,
        SwitchTo(
            Const("📜Показать аппликатуры аккордов"),
            id="to_chords_tabs",
            state=states.FoundedSongsPanelSG.song_chords_with_tabs,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.FoundedSongsPanelSG.song_menu,
        ),
        state=states.FoundedSongsPanelSG.song_chords,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords,
    ),
    Window(
        templates.SONG_CHORDS_WITH_TABS_TEMPLATE,
        SwitchTo(
            Const("📜Убрать аппликатуры аккордов"),
            id="to_chords",
            state=states.FoundedSongsPanelSG.song_chords,
        ),
        SwitchTo(
            Const("🔙Назад к меню песни"),
            id="to_song",
            state=states.FoundedSongsPanelSG.song_menu,
        ),
        state=states.FoundedSongsPanelSG.song_chords_with_tabs,
        preview_data={"song": PREVIEW_SONG},
        getter=get_chords_with_tabs,
    ),
    Window(
        Const(
            "Введите текстовое название"
        ),
        Cancel(Const("🔙Назад")),
        state=states.FoundedSongsPanelSG.message_type_error,
    ),
)
