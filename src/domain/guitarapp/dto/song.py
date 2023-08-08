from typing import List

from pydantic.main import BaseModel
from .verse import BaseVerseDTO


class BaseSongDTO(BaseModel):
    title: str
    band_id: int

    class Config:
        orm_mode = True


class CreateSongDTO(BaseSongDTO):
    verses: List[BaseVerseDTO] | None = None

#
# class CreateSongDTO(BaseSongDTO):
#     lyrics: str | None = None
#


class UpdateSongDTO(BaseModel):
    id: int
    title: str | None = None
    verses: List[BaseVerseDTO] | None = None


class SongDTO(BaseSongDTO):
    id: int


class FullSongDTO(SongDTO):
    verses: List[BaseVerseDTO]

