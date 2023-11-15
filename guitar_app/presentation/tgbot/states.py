from aiogram.fsm.state import State, StatesGroup


class MainMenuSG(StatesGroup):
    main = State()


class SongPanelSG(StatesGroup):
    menu = State()
    chords = State()
    band = State()


class SearchHistoryPanelSG(StatesGroup):
    list = State()
    song = State()
    chords = State()
    band = State()


class FavoriteSongsPanelSG(StatesGroup):
    choose_song = State()
    song = State()
    song_menu = State()
    song_chords = State()
    song_chords_with_tabs = State()
    song_tabs = State()
    song_tab_detail = State()


class AllSongsPanelSG(StatesGroup):
    choose_song = State()
    song = State()
    song_menu = State()
    song_chords = State()
    song_chords_with_tabs = State()
    song_tabs = State()
    song_tab_detail = State()


class FoundedSongsPanelSG(StatesGroup):
    input_song_title = State()
    message_type_error = State()
    choose_song = State()
    song = State()
    song_menu = State()
    song_chords = State()
    song_chords_with_tabs = State()
    song_tabs = State()
    song_tab_detail = State()


class BandSongsPanelSG(StatesGroup):
    choose_song = State()
    song = State()
    song_menu = State()
    song_chords = State()
    song_chords_with_tabs = State()
    song_tabs = State()
    song_tab_detail = State()


class AllBandsPanelSG(StatesGroup):
    choose_band = State()
    choose_song = State()
    song = State()
    song_menu = State()
    song_chords = State()
    song_chords_with_tabs = State()
    song_tabs = State()
    song_tab_detail = State()
