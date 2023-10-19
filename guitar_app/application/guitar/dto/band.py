from dataclasses import dataclass

from .musician import MusicianDTO


@dataclass
class BaseBandDTO:
    title: str


@dataclass
class CreateBandDTO(BaseBandDTO):
    pass


@dataclass
class UpdateBandDTO:
    id: int
    title: str | None


@dataclass
class BandDTO(BaseBandDTO):
    id: int


@dataclass(frozen=True)
class FullBandDTO:
    # if import in top, it will be a circular import problem (somehow idk)
    from .song import SongDTO

    id: int
    title: str
    members: list[MusicianDTO] | None
    songs: list[SongDTO] | None


@dataclass
class UpdateMusicianBandDTO:
    musician_id: int
    band_id: int
