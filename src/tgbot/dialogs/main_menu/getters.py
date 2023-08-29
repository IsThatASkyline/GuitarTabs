from src.infrastructure.db.uow import UnitOfWork
from src.application.guitarapp import services


async def get_main(**_):

    return {
        "username": "Енотик",
    }
