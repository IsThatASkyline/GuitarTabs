import pytest_asyncio

from guitar_app.application.guitar.dto import BaseVerseDTO


@pytest_asyncio.fixture(scope="function")
async def modulation_in_data():
    return [
        BaseVerseDTO(title="verse1", lyrics="lyrics", chords="Am C Dm || G"),
        BaseVerseDTO(title="verse2", lyrics="lyrics", chords="A Cm D || Gm"),
    ], 1


@pytest_asyncio.fixture(scope="function")
async def modulation_expected_data():
    return [
        BaseVerseDTO(title="verse1", lyrics="lyrics", chords="A#m C# D#m || G#"),
        BaseVerseDTO(title="verse2", lyrics="lyrics", chords="A# C#m D# || G#m"),
    ]


@pytest_asyncio.fixture(scope="function")
async def modulation_in_data2():
    return [
        BaseVerseDTO(title="verse1", lyrics="lyrics", chords="Am C Dm G"),
        BaseVerseDTO(title="verse2", lyrics="lyrics", chords="A Cm D Gm"),
    ], -2


@pytest_asyncio.fixture(scope="function")
async def modulation_expected_data2():
    return [
        BaseVerseDTO(title="verse1", lyrics="lyrics", chords="Gm A# Cm F"),
        BaseVerseDTO(title="verse2", lyrics="lyrics", chords="G A#m C Fm"),
    ]
