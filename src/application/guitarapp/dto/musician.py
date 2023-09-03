from pydantic.main import BaseModel


class BaseMusicianDTO(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class CreateMusicianDTO(BaseMusicianDTO):
    pass


class UpdateMusicianDTO(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None


class MusicianDTO(BaseMusicianDTO):
    id: int
