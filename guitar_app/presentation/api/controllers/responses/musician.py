from pydantic import BaseModel, Field


class MusicianDeleteResponse(BaseModel):
    message: str = Field("The musician has been deleted", const=True)
