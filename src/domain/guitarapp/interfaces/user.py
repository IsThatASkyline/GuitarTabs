from guitar_app.src.domain.common.usecases.base import BaseUseCase
from guitar_app.src.infrastructure.db.uow import UnitOfWork


class UserUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)
