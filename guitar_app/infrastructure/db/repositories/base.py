from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from guitar_app.infrastructure.db.models import BaseAlchemyModels

Model = TypeVar("Model", bound=BaseAlchemyModels)


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, dto):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id_):
        raise NotImplementedError

    @abstractmethod
    async def list(self):
        raise NotImplementedError

    @abstractmethod
    async def update(self, id_, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id_):
        raise NotImplementedError


class BaseRepository(Generic[Model], AbstractRepository):
    def __init__(self, model: type[Model], session: AsyncSession):
        self._model = model
        self._session = session

    async def add(self, dto) -> Model:
        ent = self._model(dto)
        self._session.add(ent)
        await self._session.flush()
        return ent

    async def get(self, id_: int) -> Model:
        query = select(self._model).where(self._model.id == id_)
        return (await self._session.execute(query)).scalar_one_or_none()

    async def list(self) -> Sequence[Model]:
        result = await self._session.execute(select(self._model).order_by(self._model.title))
        return result.scalars().all()

    async def update(self, id_: int, **kwargs) -> None:
        query = update(self._model).where(self._model.id == id_).values(kwargs)
        await self._session.execute(query)

    async def delete(self, id_: int) -> None:
        query = delete(self._model).where(self._model.id == id_)
        await self._session.execute(query)
