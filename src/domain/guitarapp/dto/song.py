from pydantic.main import BaseModel


class BaseSongDTO(BaseModel):
    title: str
    band_id: int

    class Config:
        orm_mode = True


class CreateSongDTO(BaseSongDTO):
    lyrics: str | None = None


class UpdateSongDTO(BaseModel):
    id: int
    title: str | None = None
    lyrics: str | None = None


class SongDTO(BaseSongDTO):
    id: int


class FullSongDTO(SongDTO):
    lyrics: str | None
