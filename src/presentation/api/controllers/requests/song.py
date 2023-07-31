from pydantic import BaseModel


class BaseSong(BaseModel):
    title: str
    band_id: int


class CreateSongRequest(BaseSong):
    lyrics: str


class UpdateSongRequest(BaseSong):
    id: int
    title: str | None = None
    lyrics: str | None = None
