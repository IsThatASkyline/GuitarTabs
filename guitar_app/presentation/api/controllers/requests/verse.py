from pydantic import BaseModel


class CreateVerseRequest(BaseModel):
    title: str
    lyrics: str | None = None
    chords: str | None = None
