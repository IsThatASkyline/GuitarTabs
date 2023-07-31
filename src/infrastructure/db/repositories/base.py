from typing import Generic, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models.base import BaseAlchemyModels

Model = TypeVar("Model", bound=BaseAlchemyModels)


class BaseRepository(Generic[Model]):
    def __init__(self, model: type[Model], session: AsyncSession):
        self._model = model
        self._session = session

    async def get_by_id(self, id_: int) -> Model:
        query = select(self._model).where(self._model.id == id_)
        return (await self._session.execute(query)).scalar_one_or_none()

    async def get_all(self) -> list[Model]:
        result = await self._session.execute(select(self._model))
        return result.scalars().all()

    async def update_obj(self, id_: int, **kwargs) -> None:
        query = update(self._model).where(self._model.id == id_).values(kwargs)
        await self._session.execute(query)

    async def delete_obj(self, id_: int) -> None:
        query = delete(self._model).where(self._model.id == id_)
        await self._session.execute(query)
