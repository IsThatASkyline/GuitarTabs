from pydantic import BaseModel

from .verse import CreateVerseRequest


class BaseSong(BaseModel):
    title: str
    band_id: int
    description: str | None = None


class CreateSongRequest(BaseSong):
    verses: list[CreateVerseRequest] | None = None


class UpdateSongRequest(BaseModel):
    title: str | None = None


class ModulateSongRequest(BaseModel):
    value: int


class AddFavoriteSongRequest(BaseModel):
    user_id: int


class RemoveFavoriteSongRequest(BaseModel):
    user_id: int


class FindSongRequest(BaseModel):
    value: str
