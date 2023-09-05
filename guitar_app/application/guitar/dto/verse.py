from pydantic.main import BaseModel


class BaseVerseDTO(BaseModel):
    title: str
    lyrics: str
    chords: str

    class Config:
        orm_mode = True


class CreateVerseDTO(BaseVerseDTO):
    song_id: int
