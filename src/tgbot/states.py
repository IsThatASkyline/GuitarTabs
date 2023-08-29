from aiogram.fsm.state import StatesGroup, State


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


class AllSongsPanelSG(StatesGroup):
    choose_song = State()
    song = State()
    song_menu = State()
    song_chords = State()


class BandSongsPanelSG(StatesGroup):
    choose_song = State()
    song = State()
    song_menu = State()
    song_chords = State()


class AllBandsPanelSG(StatesGroup):
    choose_band = State()
    menu = State()
    band_menu = State()
    band_song = State()
    band_song_chords = State()
