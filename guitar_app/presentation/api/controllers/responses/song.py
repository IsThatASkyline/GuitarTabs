from pydantic import BaseModel, Field


class SongCreateResponse(BaseModel):
    message: str = Field("The song has been created", const=True)


class SongDeleteResponse(BaseModel):
    message: str = Field("The song has been deleted", const=True)


class TabsDeleteResponse(BaseModel):
    message: str = Field("Tabs has been deleted", const=True)
