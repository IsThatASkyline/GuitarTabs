from dataclasses import dataclass


@dataclass(frozen=True)
class Verse:
    title: str
    lyrics: str
    chords: str
