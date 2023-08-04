from pydantic import BaseModel, Field


class BandDeleteResponse(BaseModel):
    message: str = Field("The band has been deleted", const=True)