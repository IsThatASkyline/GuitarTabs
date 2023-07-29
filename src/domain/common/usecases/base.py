from abc import ABC

from guitar_app.src.infrastructure.db.uow import UnitOfWork


class BaseUseCase(ABC):
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
