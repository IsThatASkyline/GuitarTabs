from typing import List
from src.domain.guitarapp.dto import BaseVerseDTO

major_chords_base = ('A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#')
minor_chords_base = ('Am', 'A#m', 'Bm', 'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m')

# song_chords = ['Am', 'C', 'Dm', 'G']


def modulate(song_chords: List[str], value: int) -> str:
    new_chord_sequence = []

    for i in range(len(song_chords)):
        chord = song_chords[i]
        if 'm' in chord:
            base_seq = minor_chords_base
        else:
            base_seq = major_chords_base

        index_chord = base_seq.index(chord)
        new_sequence = base_seq[index_chord:] + base_seq[:index_chord]
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