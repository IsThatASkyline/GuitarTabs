from pydantic import BaseModel, Field


class SongCreateResponse(BaseModel):
    message: str = Field("The song has been created")


class SongDeleteResponse(BaseModel):
    message: str = Field("The song has been deleted")


class TabsDeleteResponse(BaseModel):
    message: str = Field("Tabs has been deleted")
