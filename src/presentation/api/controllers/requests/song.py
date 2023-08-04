from pydantic import BaseModel


class BaseSong(BaseModel):
    title: str
    band_id: int


class CreateSongRequest(BaseSong):
    lyrics: str | None = None


class UpdateSongRequest(BaseModel):
    title: str | None = None
    lyrics: str | None = None
