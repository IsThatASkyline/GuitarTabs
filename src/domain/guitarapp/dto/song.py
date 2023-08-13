from pydantic.main import BaseModel
from .verse import BaseVerseDTO


class BaseSongDTO(BaseModel):
    title: str
    band_id: int

    class Config:
        orm_mode = True


class CreateSongDTO(BaseSongDTO):
    verses: list[BaseVerseDTO] | None = None


class UpdateSongDTO(BaseModel):
    id: int
    title: str | None = None
    verses: list[BaseVerseDTO] | None = None


class SongDTO(BaseSongDTO):
    id: int


class FullSongDTO(SongDTO):
    verses: list[BaseVerseDTO] | None


class ModulateSongDTO(BaseModel):
    id: int
    value: int


class FavoriteSongDTO(BaseModel):
    song_id: int
    user_id: int