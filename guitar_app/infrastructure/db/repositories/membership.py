from sqlalchemy.ext.asyncio import AsyncSession

from guitar_app.application.guitar.dto import UpdateMusicianBandDTO
from guitar_app.infrastructure.db.models.secondaries import BandMembers
from guitar_app.infrastructure.db.repositories.base import BaseRepository


class BandMembersRepository(BaseRepository[BandMembers]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(BandMembers, session)

    async def add(self, musician_dto: UpdateMusicianBandDTO) -> None:
        musician = BandMembers(**musician_dto.dict())
        self.session.add(musician)
        return
