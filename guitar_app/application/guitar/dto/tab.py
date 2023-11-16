from dataclasses import dataclass


@dataclass
class BaseTabDTO:
    title: str
    image_url: str


@dataclass
class CreateTabDTO:
    song_id: int
    tabs: list[BaseTabDTO]


@dataclass
class TabDTO(BaseTabDTO):
    id: int
