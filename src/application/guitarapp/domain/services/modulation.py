from typing import List
from src.application.guitarapp.dto import BaseVerseDTO
from src.application.guitarapp.domain.utils.default_constants import MAJOR_CHORDS_SEQUENCE, MINOR_CHORDS_SEQUENCE


def modulate(song_chords: List[str], value: int) -> str:
    new_chord_sequence = []

    for i in range(len(song_chords)):
        chord = song_chords[i]
        if 'm' in chord:
            base_seq = MINOR_CHORDS_SEQUENCE
        else:
            base_seq = MAJOR_CHORDS_SEQUENCE

        chord_index = base_seq.index(chord)
        new_sequence = base_seq[chord_index:] + base_seq[:chord_index]
        new_chord_sequence.append(new_sequence[value])

    return ' '.join(new_chord_sequence)


def get_modulate_verses(verses: List[BaseVerseDTO], value: int) -> List[BaseVerseDTO]:
    new_verses = []

    for verse in verses:
        old_chords = verse.chords
        new_chords = modulate(old_chords.split(), value)
        new_verses.append(
            BaseVerseDTO(title=verse.title, lyrics=verse.lyrics, chords=new_chords)
        )

    return new_verses
