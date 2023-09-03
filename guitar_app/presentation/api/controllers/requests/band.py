from pydantic.main import BaseModel


class BaseBand(BaseModel):
    title: str


class CreateBandRequest(BaseBand):
    pass


class UpdateBandRequest(BaseBand):
    pass


class UpdateMusicianBandRequest(BaseModel):
    musician_id: int
