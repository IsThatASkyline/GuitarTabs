from src.infrastructure.db.uow import UnitOfWork
from src.application.guitarapp import services


async def get_main(uow: UnitOfWork, **_):
    songs = await services.SongServices(uow).get_all_songs()
    print(songs)
    return {
        "username": "Енотик",
    }
