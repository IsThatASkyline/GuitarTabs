from pydantic import BaseModel


class BaseMusician(BaseModel):
    first_name: str | None = None
    last_name: str | None = None


class CreateMusicianRequest(BaseMusician):
    pass


class UpdateMusicianRequest(BaseMusician):
    first_name: str | None = None
    last_name: str | None = None
