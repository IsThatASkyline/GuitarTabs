from dataclasses import dataclass

from src.application.models.chord import Chord


@dataclass(frozen=True)
class Song:
    title: str
    band: str
    chords: list[Chord]
    lyrics: str