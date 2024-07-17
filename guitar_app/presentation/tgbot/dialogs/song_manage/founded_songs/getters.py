from aiogram_dialog import DialogManager

from guitar_app.application.guitar import dto, services
from guitar_app.infrastructure.db.uow import UnitOfWork


async def get_songs_founded_by_title(uow: UnitOfWork, dialog_manager: DialogManager, **_):
    song_title = (
        dialog_manager.dialog_data.get("song_title", None) or dialog_manager.start_data["song_title"]
    )
    return {
        "songs": await services.SongServices(uow).find_song(dto.FindSongDTO(value=song_title)),
        "song_title": song_title,
    }
