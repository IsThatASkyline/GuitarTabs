from guitar_app.application.guitar import services
from guitar_app.infrastructure.db.uow import UnitOfWork


async def get_all_bands(uow: UnitOfWork, **_):
    return {
        "bands": await services.BandServices(uow).get_all_bands()
    }
