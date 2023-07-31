from src.domain.common.usecases.base import BaseUseCase
from src.infrastructure.db.uow import UnitOfWork


class MusicianUseCase(BaseUseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        super().__init__(uow)
