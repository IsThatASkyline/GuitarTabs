from aiogram_dialog import DialogManager

from guitar_app.application.guitar import dto, services
from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.presentation.tgbot.jinja.chords import CHORDS_TABLATURE
from guitar_app.presentation.tgbot.models.verse import Chord, Verse, VerseString


async def get_song(uow: UnitOfWork, user: dto.UserDTO, dialog_manager: DialogManager, **_):
    song_id = dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    song = await services.SongServices(uow).get_song_by_id(id_=song_id)
    return {
        "song": await services.SongServices(uow).get_song_by_id(id_=song_id),
        "in_favorites": song.compress()
        in await services.SongServices(uow).get_favorite_songs_by_user(user_dto=user),
    }


async def get_chords(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    song_id = dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    song = await services.SongServices(uow).get_song_by_id(id_=song_id)
    verses = song.verses
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
            verse_strings = await get_verse_strings_for_full_verse(chords_list, lyrics_list)
            result.append(Verse(title=verse.title, strings=verse_strings))
        elif not lyrics_list and chords_list:
            verse_strings = await get_verse_strings_for_half_verse(chords_list)
            result.append(Verse(title=verse.title, strings=verse_strings))
        elif not lyrics_list and not chords_list:
            result.append(Verse(title=verse.title, strings=None))

    return {
        "song_title": song.title,
        "verses": result,
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
    chords_len = len(chords)
    if len(lyrics) <= 10:
        if chords_len == 0:
            space_between_chords = ' ' * 20
        elif chords_len == 1:
            space_between_chords = ' ' * 15
        elif chords_len == 2:
            space_between_chords = ' ' * 10
        elif chords_len == 3:
            space_between_chords = ' ' * 4
        elif chords_len == 4:
            space_between_chords = ' ' * 2
        else:
            space_between_chords = ' ' * 2

    elif len(lyrics) > 10 and len(lyrics) <= 15:
        if chords_len == 0:
            space_between_chords = ' ' * 30
        elif chords_len == 1:
            space_between_chords = ' ' * 20
        elif chords_len == 2:
            space_between_chords = ' ' * 12
        elif chords_len == 3:
            space_between_chords = ' ' * 6
        elif chords_len == 4:
            space_between_chords = ' ' * 4
        else:
            space_between_chords = ' ' * 2

    elif len(lyrics) > 15 and len(lyrics) <= 20:
        if chords_len == 0:
            space_between_chords = ' ' * 33
        elif chords_len == 1:
            space_between_chords = ' ' * 25
        elif chords_len == 2:
            space_between_chords = ' ' * 25
        elif chords_len == 3:
            space_between_chords = ' ' * 8
        elif chords_len == 4:
            space_between_chords = ' ' * 6
        else:
            space_between_chords = ' ' * 2

    elif len(lyrics) > 20 and len(lyrics) <= 25:
        if chords_len == 0:
            space_between_chords = ' ' * 43
        elif chords_len == 1:
            space_between_chords = ' ' * 40
        elif chords_len == 2:
            space_between_chords = ' ' * 35
        elif chords_len == 3:
            space_between_chords = ' ' * 17
        elif chords_len == 4:
            space_between_chords = ' ' * 9
        else:
            space_between_chords = ' ' * 2

    elif len(lyrics) > 25 and len(lyrics) <= 30:
        if chords_len == 0:
            space_between_chords = ' ' * 45
        elif chords_len == 1:
            space_between_chords = ' ' * 43
        elif chords_len == 2:
            space_between_chords = ' ' * 22
        elif chords_len == 3:
            space_between_chords = ' ' * 20
        elif chords_len == 4:
            space_between_chords = ' ' * 10
        elif chords_len == 5:
            space_between_chords = ' ' * 6
        else:
            space_between_chords = ' ' * 2

    elif len(lyrics) > 30:
        if chords_len == 0:
            space_between_chords = ' ' * 60
        elif chords_len == 1:
            space_between_chords = ' ' * 50
        elif chords_len == 2:
            space_between_chords = ' ' * 25
        elif chords_len == 3:
            space_between_chords = ' ' * 23
        elif chords_len == 4:
            space_between_chords = ' ' * 16
        elif chords_len == 5:
            space_between_chords = ' ' * 10
        else:
            space_between_chords = ' ' * 2

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


async def get_chords_with_tabs(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    song_id = dialog_manager.dialog_data.get("song_id", None) or dialog_manager.start_data["song_id"]
    song = await services.SongServices(uow).get_song_by_id(id_=song_id)
    verses = song.verses
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
            verse_strings, chords = await get_verse_strings_with_tabs_for_full_verse(chords_list, lyrics_list)
            unique_chords.update(chords)
            result.append(Verse(title=verse.title, strings=verse_strings))
        elif not lyrics_list and chords_list:
            verse_strings, chords = await get_verse_strings_with_tabs_for_half_verse(chords_list)
            unique_chords.update(chords)
            result.append(Verse(title=verse.title, strings=verse_strings))
        elif not lyrics_list and not chords_list:
            result.append(Verse(title=verse.title, strings=None))

    return {
        "song_title": song.title,
        "verses": result,
        "chords_tabs": [
            Chord(title=chord, tab=CHORDS_TABLATURE[f"{chord}"]) for chord in unique_chords
        ],
    }


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
