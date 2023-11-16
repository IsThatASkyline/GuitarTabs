from dataclasses import dataclass

from .band import BandDTO
from .tab import TabDTO
from .verse import BaseVerseDTO


@dataclass
class BaseSongDTO:
    title: str
    band_id: int


@dataclass
class GetSongDTO:
    song_id: int
    user_id: int | None = None


@dataclass
class CreateSongDTO(BaseSongDTO):
    verses: list[BaseVerseDTO] | None = None
    tabs: list[TabDTO] | None = None


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
    hits_count: int | None
    tabs: list[TabDTO] | None = None

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
