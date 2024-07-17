from guitar_app.application.guitar import services
from guitar_app.infrastructure.db.uow import UnitOfWork


async def get_all_songs(uow: UnitOfWork, **_):
    return {
        "songs": await services.SongServices(uow).get_all_songs(),
    }
