from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from guitar_app.application.guitar import dto, services
from guitar_app.application.guitar.domain.services.modulation import (
    get_modulated_verses,
)
from guitar_app.application.guitar.dto import GetSongDTO
from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.presentation.tgbot.jinja.chords import CHORDS_TABLATURE
from guitar_app.presentation.tgbot.models.verse import Chord, Verse, VerseString
from guitar_app.presentation.tgbot.utils import space_ranges


async def get_chords(uow: UnitOfWork, user: dto.UserDTO, dialog_manager: DialogManager, **_):
    song_id = dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    song = await services.SongServices(uow).get_song_by_id(
        GetSongDTO(
            song_id=song_id,
            user_id=user.telegram_id,
        )
    )

    mod_value = dialog_manager.dialog_data.get("mod_value", None)
    if not mod_value == 0:
        new_verses = get_modulated_verses(song.verses, mod_value)
        verses, unique_chords = await _get_verses_and_unique_chords(new_verses)
        chords_tabs = await get_chords_tabs(unique_chords)
    else:
        verses, unique_chords = await _get_verses_and_unique_chords(song.verses)
        chords_tabs = await get_chords_tabs(unique_chords)
    return {"song": song, "verses": verses, "chords_tabs": chords_tabs, "mod_value": mod_value}


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


async def get_chords_tabs(chords):
    chords_tabs = []
    for chord in chords:
        try:
            chords_tabs.append(Chord(title=chord, tab=CHORDS_TABLATURE[f"{chord}"]))
        except KeyError:
            pass
    return chords_tabs


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


async def get_verse_strings_for_full_verse(chords_list, lyrics_list):
    verse_strings = []
    for chords, lyrics in zip(*(chords_list, lyrics_list)):
        if " || " in chords:
            chords, end_chords = chords.split("||")
            end_chords = [Chord(title=chord) for chord in end_chords.split()]
        else:
            end_chords = None

        chords = [Chord(title=chord) for chord in chords.split()]
        space_between_chords = await get_space_between(lyrics, chords)
        pair = VerseString(
            lyrics=lyrics,
            chords=chords,
            end_chords=end_chords,
            chords_count=len(chords),
            space_between_chords=space_between_chords,
        )
        verse_strings.append(pair)
    return verse_strings


async def get_space_between(lyrics, chords):
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


async def get_verse_strings_for_half_verse(chords_list):
    verse_strings = []
    for chords in chords_list:
        verse_string_chords = [Chord(title=chord) for chord in chords.split()]
        pair = VerseString(
            lyrics=None,
            chords=verse_string_chords,
        )
        verse_strings.append(pair)
    return verse_strings


async def get_verse_strings_with_tabs_for_full_verse(chords_list, lyrics_list):
    verse_strings = []
    unique_chords = set()
    for chords, lyrics in zip(*(chords_list, lyrics_list)):
        all_chords_in_verse_string = chords[:].replace("||", "").split()
        unique_chords.update(all_chords_in_verse_string)
        if "||" in chords:
            chords, end_chords = chords.split("||")
            end_chords = [Chord(title=chord) for chord in end_chords.split()]
        else:
            end_chords = None

        chords = [Chord(title=chord) for chord in chords.split()]
        space_between_chords = await get_space_between(lyrics, chords)
        pair = VerseString(
            lyrics=lyrics,
            chords=chords,
            end_chords=end_chords,
            chords_count=len(chords),
            space_between_chords=space_between_chords,
        )
        verse_strings.append(pair)
    return verse_strings, unique_chords


async def get_verse_strings_with_tabs_for_half_verse(chords_list):
    verse_strings = []
    unique_chords = set()
    for chords in chords_list:
        all_chords_in_verse_string = chords.split()
        unique_chords.update(all_chords_in_verse_string)
        verse_string_chords = [Chord(title=chord) for chord in chords.split()]
        pair = VerseString(
            lyrics=None,
            chords=verse_string_chords,
            chords_count=len(verse_string_chords),
        )
        verse_strings.append(pair)
    return verse_strings, unique_chords


async def _get_verses_and_unique_chords(verses):
    result = []
    unique_chords = set()
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
            verse_strings, chords = await get_verse_strings_with_tabs_for_full_verse(
                chords_list, lyrics_list
            )
            unique_chords.update(chords)
            result.append(Verse(title=verse.title, strings=verse_strings))
        elif not lyrics_list and chords_list:
            verse_strings, chords = await get_verse_strings_with_tabs_for_half_verse(chords_list)
            unique_chords.update(chords)
            result.append(Verse(title=verse.title, strings=verse_strings))
        elif not lyrics_list and not chords_list:
            result.append(Verse(title=verse.title, strings=None))
    return result, unique_chords
