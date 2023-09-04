from pydantic import BaseModel


class CreateVerseRequest(BaseModel):
    title: str
    lyrics: str
    chords: str
