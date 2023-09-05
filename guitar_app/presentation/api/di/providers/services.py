from fastapi import Depends

from guitar_app.application.guitar.services import (
    BandServices,
    MusicianServices,
    SongServices,
    UserServices,
)
from guitar_app.infrastructure.db.uow import UnitOfWork
from guitar_app.presentation.api.di.providers.db import uow_provider


def get_user_services(uow: UnitOfWork = Depends(uow_provider)) -> UserServices:
    return UserServices(uow)


def get_musician_services(
    uow: UnitOfWork = Depends(uow_provider),
) -> MusicianServices:
    return MusicianServices(uow)


def get_song_services(uow: UnitOfWork = Depends(uow_provider)) -> SongServices:
    return SongServices(uow)


def get_band_services(uow: UnitOfWork = Depends(uow_provider)) -> BandServices:
    return BandServices(uow)
