import pytest_asyncio

from src.application.models.verse import Verse
from src.domain.guitarapp.dto import BaseVerseDTO


@pytest_asyncio.fixture(scope='function')
async def in_data():
    return [Verse('verse1', 'lyrics', 'Am C Dm G'), Verse('verse2', 'lyrics', 'A Cm D Gm')], 1


@pytest_asyncio.fixture(scope='function')
async def expected_data():
    return [BaseVerseDTO(title='verse1', lyrics='lyrics', chords='A#m C# D#m G#'),
            BaseVerseDTO(title='verse2', lyrics='lyrics', chords='A# C#m D# G#m')]


@pytest_asyncio.fixture(scope='function')
async def in_data2():
    return [Verse('verse1', 'lyrics', 'Am C Dm G'), Verse('verse2', 'lyrics', 'A Cm D Gm')], -2


@pytest_asyncio.fixture(scope='function')
async def expected_data2():
    return [BaseVerseDTO(title='verse1', lyrics='lyrics', chords='Gm A# Cm F'),
            BaseVerseDTO(title='verse2', lyrics='lyrics', chords='G A#m C Fm')]
