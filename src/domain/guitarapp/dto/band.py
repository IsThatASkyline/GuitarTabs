from typing import List
from pydantic.main import BaseModel
from .musician import MusicianDTO
from .song import SongDTO


class BaseBandDTO(BaseModel):
    title: str

    class Config:
        orm_mode = True


class CreateBandDTO(BaseBandDTO):
    pass


class UpdateBandDTO(BaseBandDTO):
    id: int
    title: str | None


class BandDTO(BaseBandDTO):
    id: int


class FullBandDTO(BaseBandDTO):
    id: int
    members: List[MusicianDTO] | None
    songs: List[SongDTO] | None


class UpdateMusicianBandDTO(BaseModel):
    musician_id: int
    band_id: int
