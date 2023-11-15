from pydantic import BaseModel


class BaseTab(BaseModel):
    title: str
    image_url: str


class CreateTabRequest(BaseTab):
    pass
