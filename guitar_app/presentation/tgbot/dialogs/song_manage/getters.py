from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from guitar_app.application.guitar import dto, services
from guitar_app.application.guitar.domain.services.modulation import (
    get_modulated_verses,
)
from guitar_app.application.guitar.dto import GetSongDTO, BaseVerseDTO
from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.presentation.tgbot.jinja.chords import CHORDS_TABLATURE
from guitar_app.presentation.tgbot.models.verse import Chord, Verse, VerseString
from guitar_app.presentation.tgbot.utils import space_ranges


async def get_song(uow: UnitOfWork, user: dto.UserDTO, dialog_manager: DialogManager, **_):
    song_id = dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    song = await services.SongServices(uow).get_song_by_id(
        GetSongDTO(
            song_id=song_id,
            user_id=user.telegram_id,
        )
    )
    return {
        "song": song,
        "in_favorites": song.compress()
        in await services.SongServices(uow).get_favorite_songs_by_user(user_dto=user),
    }


async def get_chords(uow: UnitOfWork, user: dto.UserDTO, dialog_manager: DialogManager, **_):
    song_id = dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    song = await services.SongServices(uow).get_song_by_id(
        GetSongDTO(
            song_id=song_id,
            user_id=user.telegram_id,
        )
    )

    mod_value = dialog_manager.dialog_data.get("mod_value")
    if mod_value:
        new_verses = await get_modulated_verses(song.verses, mod_value)
        verses = await _get_verses(new_verses)
    else:
        verses = await _get_verses(song.verses)
    return {
        "song": song,
        "verses": verses,
        "mod_value": mod_value,
    }


async def get_fingerings(uow: UnitOfWork, user: dto.UserDTO, dialog_manager: DialogManager, **_):
    song_id = dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    song = await services.SongServices(uow).get_song_by_id(
        GetSongDTO(
            song_id=song_id,
            user_id=user.telegram_id,
        )
    )

    mod_value = dialog_manager.dialog_data.get("mod_value")
    if mod_value:
        new_verses = await get_modulated_verses(song.verses, mod_value)
        unique_chords = await _get_unique_chords(new_verses)
        chords_fingerings = await _get_chords_fingerings(unique_chords)
    else:
        unique_chords = await _get_unique_chords(song.verses)
        chords_fingerings = await _get_chords_fingerings(unique_chords)
    return {
        "song": song,
        "chords_fingerings": chords_fingerings,
        "mod_value": mod_value,
    }


async def get_all_tabs(uow: UnitOfWork, user: dto.UserDTO, dialog_manager: DialogManager, **_):
    song_id = dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]

    song = await services.SongServices(uow).get_song_by_id(
        GetSongDTO(song_id=song_id, user_id=user.id)
    )
    return {"tabs": song.tabs, "song_title": song.title, "band_title": song.band.title}


async def get_detail_tab(uow: UnitOfWork, user: dto.UserDTO, dialog_manager: DialogManager, **_):
    tab_id = dialog_manager.dialog_data.get("tab_id", None) or dialog_manager.start_data["tab_id"]
    tab = await services.SongServices(uow).get_tab(tab_id)
    tab_image = MediaAttachment(ContentType.PHOTO, url=tab.image_url)
    return {"tab": tab_image, "title": tab.title}


async def _get_verses(verses):
    result = []
    for verse in verses:
        try:
            chords_list = verse.chords.split("//")
        except AttributeError:
            chords_list = None
        try:
            lyrics_list = verse.lyrics.split("//")
        except AttributeError:
            lyrics_list = None

        if lyrics_list and chords_list:
            verse_strings = await _get_verse_strings(
                chords_list, lyrics_list
            )
            result.append(Verse(title=verse.title, strings=verse_strings))
        elif not lyrics_list and chords_list:
            verse_strings = await _get_verse_strings_without_lyrics(
                chords_list
            )
            result.append(Verse(title=verse.title, strings=verse_strings))
        elif lyrics_list and not chords_list:
            verse_strings = await _get_verse_strings_without_chords(
                lyrics_list
            )
            result.append(Verse(title=verse.title, strings=verse_strings))
        elif not lyrics_list and not chords_list:
            result.append(Verse(title=verse.title, strings=None))
    return result


async def _get_chords_fingerings(chords: set[str]) -> list[Chord]:
    chords_fingerings = []
    for chord in chords:
        try:
            chords_fingerings.append(Chord(title=chord, tab=CHORDS_TABLATURE[f"{chord}"]))
        except KeyError:
            # В случае, когда не добавлена аппликатура к аккорду
            pass
    return chords_fingerings


async def _get_verse_strings(chords_list, lyrics_list):
    verse_strings = []
    for chords, lyrics in zip(*(chords_list, lyrics_list)):
        if "||" in chords:
            chords, end_chords = chords.split("||")
            end_chords = [Chord(title=chord) for chord in end_chords.split()]
        else:
            end_chords = None

        chords = [Chord(title=chord) for chord in chords.split()]
        space_between_chords = await _get_space_between(lyrics, chords)
        pair = VerseString(
            lyrics=lyrics,
            chords=chords,
            end_chords=end_chords,
            chords_count=len(chords),
            space_between_chords=space_between_chords,
        )
        verse_strings.append(pair)
    return verse_strings


async def _get_unique_chords(verses: list[BaseVerseDTO]):
    unique_chords = set()
    for verse in verses:
        all_chords_in_verse_string = verse.chords.replace("||", " ").replace("//", " ").split()
        unique_chords.update(all_chords_in_verse_string)
    return unique_chords


async def _get_verse_strings_without_lyrics(chords_list):
    verse_strings = []
    for chords in chords_list:
        verse_string_chords = [Chord(title=chord) for chord in chords.split()]
        pair = VerseString(
            lyrics=None,
            chords=verse_string_chords,
            chords_count=len(verse_string_chords),
        )
        verse_strings.append(pair)
    return verse_strings


async def _get_verse_strings_without_chords(lyrics_list):
    verse_strings = []
    for lyrics in lyrics_list:
        verse_string = VerseString(
            lyrics=lyrics
        )
        verse_strings.append(verse_string)
    return verse_strings


async def _get_space_between(lyrics, chords):
    lyrics_len = len(lyrics)
    chords_len = len(chords)

    if lyrics_len <= 10:
        space_between_chords = space_ranges.space_less_10[chords_len]
    elif 10 < lyrics_len <= 15:
        space_between_chords = space_ranges.space_more_10_less_15[chords_len]
    elif 15 < lyrics_len <= 20:
        space_between_chords = space_ranges.space_more_15_less_20[chords_len]
    elif 20 < lyrics_len <= 25:
        space_between_chords = space_ranges.space_more_20_less_25[chords_len]
    elif 25 < lyrics_len <= 30:
        space_between_chords = space_ranges.space_more_25_less_30[chords_len]
    elif lyrics_len > 30:
        space_between_chords = space_ranges.space_more_30[chords_len]
    else:
        space_between_chords = " " * 2

    return space_between_chords
