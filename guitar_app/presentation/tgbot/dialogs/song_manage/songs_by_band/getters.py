from aiogram_dialog import DialogManager

from guitar_app.application.guitar import services
from guitar_app.infrastructure.db.uow import UnitOfWork


async def get_songs_by_band(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    band_id = dialog_manager.dialog_data.get("band_id", None) or dialog_manager.start_data["band_id"]
    band = await services.BandServices(uow).get_band_by_id(id_=band_id)
    return {
        "songs": await services.SongServices(uow).get_songs_by_band(band_id=band_id),
        "band_title": band.title,
    }
