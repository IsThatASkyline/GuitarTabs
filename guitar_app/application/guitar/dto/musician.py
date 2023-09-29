from dataclasses import dataclass


@dataclass
class BaseMusicianDTO:
    first_name: str
    last_name: str


@dataclass
class CreateMusicianDTO(BaseMusicianDTO):
    pass


@dataclass
class UpdateMusicianDTO:
    id: int
    first_name: str | None = None
    last_name: str | None = None


@dataclass
class MusicianDTO(BaseMusicianDTO):
    id: int
