from pydantic import BaseModel
from .verse import CreateVerseRequest


class BaseSong(BaseModel):
    title: str
    band_id: int


class CreateSongRequest(BaseSong):
    verses: list[CreateVerseRequest] | None = None


class UpdateSongRequest(BaseModel):
    title: str | None = None
    lyrics: str | None = None


class ModulateSongRequest(BaseModel):
    value: int

