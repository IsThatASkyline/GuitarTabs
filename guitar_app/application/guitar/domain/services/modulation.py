from guitar_app.application.guitar.domain.utils.default_constants import (
    MAJOR_7_CHORDS_SEQUENCE,
    MAJOR_CHORDS_SEQUENCE,
    MINOR_7_CHORDS_SEQUENCE,
    MINOR_CHORDS_SEQUENCE,
    STANDARD_CHORDS,
    SUS2_CHORDS_SEQUENCE
)
from guitar_app.application.guitar.dto import BaseVerseDTO


async def modulate(song_chords: list[str], value: int) -> str:
    new_chord_sequence = []
    for verse_line in song_chords:
        verse_line_chords = verse_line.split()
        new_verse_line_chords = []
        for i in range(len(verse_line_chords)):
            chord = verse_line_chords[i]
            if chord == "||":
                new_verse_line_chords.append("||")
                continue
            elif "sus2" in chord:
                base_seq = SUS2_CHORDS_SEQUENCE
            elif "m7" in chord:
                base_seq = MINOR_7_CHORDS_SEQUENCE
            elif "7" in chord:
                base_seq = MAJOR_7_CHORDS_SEQUENCE
            elif "m" in chord:
                base_seq = MINOR_CHORDS_SEQUENCE
            else:
                base_seq = MAJOR_CHORDS_SEQUENCE

            try:
                chord_index = base_seq.index(chord)
            except ValueError:
                chord_index = base_seq.index(await refactor_chord_to_standard(chord))

            new_sequence = base_seq[chord_index:] + base_seq[:chord_index]
            new_verse_line_chords.append(new_sequence[value])
        new_chord_sequence.append(" ".join(new_verse_line_chords))
    return "//".join(new_chord_sequence)


async def get_modulated_verses(verses: list[BaseVerseDTO], value: int) -> list[BaseVerseDTO]:
    new_verses = []
    for verse in verses:
        if verse.chords:
            old_chords = verse.chords.split("//")
            new_chords = await modulate(old_chords, value)
            new_verses.append(
                BaseVerseDTO(title=verse.title, lyrics=verse.lyrics, chords=new_chords)
            )
        else:
            new_verses.append(verse)
    return new_verses


async def refactor_chord_to_standard(chord: str):
    return STANDARD_CHORDS[chord]
