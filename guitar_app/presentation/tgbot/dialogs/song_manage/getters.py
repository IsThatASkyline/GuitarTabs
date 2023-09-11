from aiogram_dialog import DialogManager

from guitar_app.application.guitar import dto, services
from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.presentation.tgbot.jinja.chords import CHORDS_TABLATURE
from guitar_app.presentation.tgbot.models.verse import Chord, Verse, VerseString
from guitar_app.presentation.tgbot.utils import space_ranges


async def get_chords(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    song_id = dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    song = await services.SongServices(uow).get_song_by_id(id_=song_id)
    result = []
    unique_chords = set()
    for verse in song.verses:
        try:
            chords_list = verse.chords.split("//")
        except AttributeError:
            chords_list = None
        try:
            lyrics_list = verse.lyrics.split("//")
        except AttributeError:
            lyrics_list = None

        if lyrics_list and chords_list:
            verse_strings, chords = await get_verse_strings_with_tabs_for_full_verse(chords_list, lyrics_list)
            unique_chords.update(chords)
            result.append(Verse(title=verse.title, strings=verse_strings))
        elif not lyrics_list and chords_list:
            verse_strings, chords = await get_verse_strings_with_tabs_for_half_verse(chords_list)
            unique_chords.update(chords)
            result.append(Verse(title=verse.title, strings=verse_strings))
        elif not lyrics_list and not chords_list:
            result.append(Verse(title=verse.title, strings=None))

    chords_tabs = await get_chords_tabs(unique_chords)

    return {
        "song_title": song.title,
        "verses": result,
        "chords_tabs": chords_tabs,
    }


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
    song = await services.SongServices(uow).get_song_by_id(id_=song_id)
    return {
        "song": await services.SongServices(uow).get_song_by_id(id_=song_id),
        "in_favorites": song.compress()
        in await services.SongServices(uow).get_favorite_songs_by_user(user_dto=user),
    }


async def get_verse_strings_for_full_verse(chords_list, lyrics_list):
    verse_strings = []
    for chords, lyrics in zip(*(chords_list, lyrics_list)):
        if ' || ' in chords:
            chords, end_chords = chords.split('||')
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
            space_between_chords=space_between_chords
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
        space_between_chords = ' ' * 2

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
        all_chords_in_verse_string = chords[:].replace('||', '').split()
        unique_chords.update(all_chords_in_verse_string)
        if ' || ' in chords:
            chords, end_chords = chords.split(' || ')
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
            space_between_chords=space_between_chords
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


async def get_all_songs(uow: UnitOfWork, **_):
    return {
        "songs": await services.SongServices(uow).get_all_songs(),
    }


async def get_songs_by_band(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    band_id = dialog_manager.dialog_data.get("band_id", None) or dialog_manager.start_data["band_id"]
    band = await services.BandServices(uow).get_band_by_id(id_=band_id)
    return {
        "songs": await services.SongServices(uow).get_songs_by_band(band_id=band_id),
        "band_title": band.title,
    }


async def get_favorite_songs(uow: UnitOfWork, user: dto.UserDTO, **_):
    return {
        "songs": await services.SongServices(uow).get_favorite_songs_by_user(user_dto=user),
    }


async def get_songs_founded_by_title(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    song_title = (
        dialog_manager.dialog_data.get("song_title", None) or dialog_manager.start_data["song_title"]
    )
    return {
        "songs": await services.SongServices(uow).find_song(dto.FindSongDTO(value=song_title)),
        "song_title": song_title,
    }
