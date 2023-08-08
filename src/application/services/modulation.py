from typing import List
from src.application.models.chord import Chord

major_chords_base = ('A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#')
minor_chords_base = ('Am', 'A#m', 'Bm', 'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m')

song_chords = ['Am', 'C', 'Dm', 'G']


def modulation(song_chords: List[Chord], direction: bool):
    new_chord_sequence = []

    for i in range(len(song_chords)):
        chord = song_chords[i]
        if 'm' in chord:
            base_seq = minor_chords_base
        else:
            base_seq = major_chords_base

        index_chord = base_seq.index(chord)
        new_sequence = base_seq[index_chord:] + base_seq[:index_chord]
        new_chord_sequence.append(new_sequence[1 if direction else -1])

    return new_chord_sequence


