from aiogram_dialog import DialogManager

from src.infrastructure.db.uow import UnitOfWork
from src.application.guitarapp import services
from src.tgbot.models.verse import Chord, VerseString


async def get_song(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    song_id = (
        dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    )
    return {
        "song": await services.SongServices(uow).get_song_by_id(id_=song_id)
    }


async def get_chords(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    song_id = (
        dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    )
    song = await services.SongServices(uow).get_song_by_id(id_=song_id)
    verses = song.verses
    result = []
    for verse in verses:
        chords_list = verse.chords.split('\\')
        lyrics_list = verse.lyrics.split('\\')
        for chords, lyrics in zip(*(chords_list, lyrics_list)):
            verse_string_chords = [Chord(title=chord) for chord in chords.split()]
            pair = VerseString(lyrics=lyrics.strip(), chords=verse_string_chords, chords_count=len(verse_string_chords))
            result.append(pair)
    return {
        "verses_strings": result,
    }


async def get_all_songs(uow: UnitOfWork, **_):
    return {
        "songs": await services.SongServices(uow).get_all_songs()
    }


async def get_songs_by_band(**_):
    return {
        "songs": [
            {
                "id": 1,
                "title": "bandsong1",
            },
            {
                "id": 2,
                "title": "bandsong2",
            },
            {
                "id": 3,
                "title": "bandsong3",
            },
        ],
    }


async def get_favorite_songs(**_):
    return {
        "songs": [
            {
                "id": 1,
                "title": "favsong1",
            },
            {
                "id": 2,
                "title": "favsong2",
            },
        ],
    }

