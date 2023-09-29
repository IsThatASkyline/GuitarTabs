from dataclasses import dataclass


@dataclass
class BaseVerseDTO:
    title: str
    lyrics: str | None
    chords: str | None


@dataclass
class CreateVerseDTO(BaseVerseDTO):
    song_id: int
