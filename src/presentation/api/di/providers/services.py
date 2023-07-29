from fastapi import Depends

from guitar_app.src.domain.guitarapp.usecases import MusicianServices, UserServices
from guitar_app.src.infrastructure.db.uow import UnitOfWork
from guitar_app.src.presentation.api.di.providers.db import uow_provider


def get_user_services(uow: UnitOfWork = Depends(uow_provider)) -> UserServices:
    return UserServices(uow)


def get_musician_services(uow: UnitOfWork = Depends(uow_provider)) -> MusicianServices:
    return MusicianServices(uow)
