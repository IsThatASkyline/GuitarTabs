from pydantic import BaseModel, Field


class SongDeleteResponse(BaseModel):
    message: str = Field("The song has been deleted", const=True)