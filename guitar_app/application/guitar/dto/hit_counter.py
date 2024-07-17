import datetime
import time
from dataclasses import dataclass


@dataclass
class BaseHitDTO:
    song_id: int
    user_id: int


@dataclass
class CreateHitDTO(BaseHitDTO):
    pass


@dataclass
class HitDTO(BaseHitDTO):
    id: int
    created_at: datetime.datetime

    @property
    def can_be_hit(self) -> bool:
        return (time.time() - self.created_at.timestamp()) > 5 * 60
