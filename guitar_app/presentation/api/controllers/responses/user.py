from pydantic import BaseModel, Field


class UserDeleteResponse(BaseModel):
    message: str = Field("The user has been deleted", const=True)
