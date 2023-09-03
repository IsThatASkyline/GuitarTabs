from pydantic.main import BaseModel
from .musician import MusicianDTO


class BaseBandDTO(BaseModel):
    title: str

    class Config:
        orm_mode = True


class CreateBandDTO(BaseBandDTO):
    pass


class UpdateBandDTO(BaseModel):
    id: int
    title: str | None


class BandDTO(BaseBandDTO):
    id: int


class FullBandDTO(BandDTO):
    # if import in top, it will be a circular import problem (somehow idk)
    from .song import SongDTO

    members: list[MusicianDTO] | None
    songs: list[SongDTO] | None


class UpdateMusicianBandDTO(BaseModel):
    musician_id: int
    band_id: int
