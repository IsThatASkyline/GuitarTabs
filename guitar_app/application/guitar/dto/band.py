from dataclasses import dataclass


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
    songs: list[SongDTO] | None
