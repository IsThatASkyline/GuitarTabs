from dataclasses import dataclass

from .band import BandDTO
from .verse import BaseVerseDTO


@dataclass
class BaseSongDTO:
    title: str
    band_id: int


@dataclass
class CreateSongDTO(BaseSongDTO):
    verses: list[BaseVerseDTO] | None = None


@dataclass
class UpdateSongDTO:
    id: int
    title: str | None = None
    verses: list[BaseVerseDTO] | None = None


@dataclass
class SongDTO:
    id: int
    title: str
    band: BandDTO


@dataclass
class FullSongDTO:
    id: int
    title: str
    band: BandDTO
    verses: list[BaseVerseDTO]

    def compress(self):
        return SongDTO(id=self.id, title=self.title, band=self.band)


@dataclass
class ModulateSongDTO:
    id: int
    value: int


@dataclass
class FavoriteSongDTO:
    song_id: int
    user_id: int


@dataclass
class FindSongDTO:
    value: str
