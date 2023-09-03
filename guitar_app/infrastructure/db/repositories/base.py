from typing import Generic, TypeVar, Sequence
from abc import ABC, abstractmethod
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from guitar_app.infrastructure.db.models import BaseAlchemyModels

Model = TypeVar("Model", bound=BaseAlchemyModels)


class AbstractRepository(ABC):

    @abstractmethod
    async def create_obj(self, dto):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id_: int):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update_obj(self, id_: int, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_obj(self, id_: int):
        raise NotImplementedError


class BaseRepository(Generic[Model], AbstractRepository):
    def __init__(self, model: type[Model], session: AsyncSession):
        self._model = model
        self._session = session

    async def create_obj(self, dto) -> Model:
        ent = self._model(dto)
        self._session.add(ent)
        await self._session.flush()
        return ent

    async def get_by_id(self, id_: int) -> Model | None:
        query = select(self._model).where(self._model.id == id_)
        return (await self._session.execute(query)).scalar_one_or_none()

    async def get_all(self) -> Sequence[Model] | None:
        result = await self._session.execute(select(self._model))
        return result.scalars().all()

    async def update_obj(self, id_: int, **kwargs) -> None:
        query = update(self._model).where(self._model.id == id_).values(kwargs)
        await self._session.execute(query)

    async def delete_obj(self, id_: int) -> None:
        query = delete(self._model).where(self._model.id == id_)
        await self._session.execute(query)
