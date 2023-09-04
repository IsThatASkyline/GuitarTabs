from pydantic import BaseModel, Field


class BandCreateResponse(BaseModel):
    message: str = Field("The band has been created", const=True)


class BandDeleteResponse(BaseModel):
    message: str = Field("The band has been deleted", const=True)
