from abc import ABC
from guitar_app.infrastructure.db.uow import AbstractUnitOfWork


class BaseUseCase(ABC):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow
