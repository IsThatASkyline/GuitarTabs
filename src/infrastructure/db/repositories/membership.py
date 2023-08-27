from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.guitarapp.dto import CreateSongDTO, SongDTO, FullSongDTO, FavoriteSongDTO, UpdateMusicianBandDTO
from src.infrastructure.db.models.secondaries import BandMembers
from src.infrastructure.db.repositories.base import BaseRepository


class BandMembersRepository(BaseRepository[BandMembers]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(BandMembers, session)

    async def create_obj(self, musician_dto: UpdateMusicianBandDTO) -> None:
        musician = BandMembers(**musician_dto.dict())
        self.session.add(musician)
