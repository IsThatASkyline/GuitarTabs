from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from guitar_app.application.guitar.dto import (
    CreateTabDTO, TabDTO
)
from guitar_app.infrastructure.db.models import Song, Tab
from guitar_app.infrastructure.db.repositories.base import BaseRepository


class TabRepository(BaseRepository[Tab]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        super().__init__(Song, session)

    async def add_tab(self, tab_dto: CreateTabDTO):
        for tab in tab_dto.tabs:
            item = Tab(
                title=tab.title,
                song_id=tab_dto.song_id,
                image_url=tab.image_url
            )
            self.session.add(item)
            await self.session.flush()

    async def get_tab(self, id_: int) -> TabDTO:
        query = select(Tab).where(Tab.id == id_)
        tab = (await self.session.execute(query)).unique().scalar_one_or_none()
        return tab.to_dto() if tab else None

    async def delete_all_tabs_in_song(self, id_: int):
        query = delete(Song.tabs).where(Song.id == id_)
        await self.session.execute(query)

