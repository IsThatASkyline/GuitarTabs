from aiogram_dialog import DialogManager

from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.application.guitar import services, dto
from guitar_app.tgbot.models.verse import Chord, VerseString, Verse
from guitar_app.tgbot.jinja.chords import CHORDS_TABULATURE


async def get_song(uow: UnitOfWork, user: dto.UserDTO, dialog_manager: DialogManager, **_):
    song_id = (
        dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    )
    song = await services.SongServices(uow).get_song_by_id(id_=song_id)
    return {
        "song": await services.SongServices(uow).get_song_by_id(id_=song_id),
        "in_favorites": song.compress() in await services.SongServices(uow).get_favorite_songs_by_user(user_dto=user),
    }


async def get_chords(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    song_id = (
        dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    )
    song = await services.SongServices(uow).get_song_by_id(id_=song_id)
    verses = song.verses
    result = []
    # O(n2), thinking of more optimized solution
    for verse in verses:
        chords_list = verse.chords.split('\\')
        lyrics_list = verse.lyrics.split('\\')
        verse_strings = []
        for chords, lyrics in zip(*(chords_list, lyrics_list)):
            verse_string_chords = [Chord(title=chord) for chord in chords.split()]
            pair = VerseString(lyrics=lyrics.strip(), chords=verse_string_chords, chords_count=len(verse_string_chords))
            verse_strings.append(pair)
        result.append(Verse(title=verse.title, strings=verse_strings))
    return {
        "verses": result,
    }


async def get_chords_with_tabs(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    song_id = (
        dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    )
    song = await services.SongServices(uow).get_song_by_id(id_=song_id)
    verses = song.verses
    result = []
    # O(n2), thinking of more optimized solution
    unique_chords = set()
    for verse in verses:
        chords_list = verse.chords.split('\\')
        lyrics_list = verse.lyrics.split('\\')
        verse_strings = []
        for chords, lyrics in zip(*(chords_list, lyrics_list)):
            all_chords_in_verse_string = chords.split()
            unique_chords.update(all_chords_in_verse_string)
            verse_string_chords = [Chord(title=chord) for chord in all_chords_in_verse_string]
            pair = VerseString(lyrics=lyrics.strip(), chords=verse_string_chords, chords_count=len(verse_string_chords))
            verse_strings.append(pair)
        result.append(Verse(title=verse.title, strings=verse_strings))
    return {
        "verses": result,
        'chords_tabs': [
            Chord(
                title=chord,
                tab=CHORDS_TABULATURE[f'{chord}']
            ) for chord in unique_chords
        ],
    }


async def get_all_songs(uow: UnitOfWork, **_):
    return {
        "songs": await services.SongServices(uow).get_all_songs()
    }


async def get_songs_by_band(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    band_id = (
        dialog_manager.dialog_data.get("band_id", None) or dialog_manager.start_data["band_id"]
    )
    return {
        "songs": await services.SongServices(uow).get_songs_by_band(band_id=band_id)
    }


async def get_favorite_songs(uow: UnitOfWork, user: dto.UserDTO, **_):
    return {
        "songs": await services.SongServices(uow).get_favorite_songs_by_user(user_dto=user)
    }


async def get_songs_founded_by_title(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    song_title = (
        dialog_manager.dialog_data.get("song_title", None) or dialog_manager.start_data["song_title"]
    )
    return {
        "songs": await services.SongServices(uow).find_song(dto.FindSongDTO(value=song_title)),
        "song_title": song_title,
    }
