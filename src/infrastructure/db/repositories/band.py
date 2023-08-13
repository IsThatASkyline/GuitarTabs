from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.guitarapp.dto import CreateBandDTO, UpdateMusicianBandDTO, FullBandDTO, BandDTO
from src.infrastructure.db.models import Band, BandMembers, Musician, Song
from src.infrastructure.db.repositories.base import BaseRepository


class BandRepository(BaseRepository[Band]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Band, session)

    async def create_obj(self, band_dto: CreateBandDTO) -> FullBandDTO:
        band = Band(
            title=band_dto.title,
        )
        self.session.add(band)
        await self.session.flush()
        return band.to_full_dto()

    async def get_by_id(self, id_: int) -> FullBandDTO:
        # refactor into one query

        query = select(Band).where(Band.id == id_)
        band = (await self._session.execute(query)).scalar_one_or_none()

        query = select(Musician).join(BandMembers).where(BandMembers.band_id == id_)
        members = (await self._session.execute(query)).scalars().all()

        query = select(Song).where(Song.band_id == id_)
        songs = (await self._session.execute(query)).scalars().all()

        return band.to_full_dto(members=members, songs=songs) if band else None

    async def get_all(self) -> list[BandDTO]:
        bands = await super().get_all()
        return [band.to_dto() for band in bands] if bands else None

    async def update_obj(self, id_: int, **kwargs) -> None:
        await super().update_obj(id_, **kwargs)


    async def delete_obj(self, id_: int):
        await super().delete_obj(id_)
