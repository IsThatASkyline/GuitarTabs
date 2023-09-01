from dataclasses import dataclass


@dataclass
class Chord:
    title: str


@dataclass
class VerseString:
    lyrics: str
    chords: list[Chord]
    chords_count: int


@dataclass
class Verse:
    title: str
    strings: list[VerseString]
