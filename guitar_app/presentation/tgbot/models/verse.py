from dataclasses import dataclass


@dataclass
class Chord:
    title: str
    tab: str | None = None


@dataclass
class VerseString:
    chords_count: int | None = None
    space_between_chords: str | None = None
    chords: list[Chord] | None = None
    end_chords: list[Chord] | None = None
    lyrics: str | None = None


@dataclass
class Verse:
    title: str
    strings: list[VerseString] | None
