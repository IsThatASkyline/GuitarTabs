from guitar_app.application.guitar import dto, services
from guitar_app.infrastructure.db.uow import UnitOfWork


async def get_favorite_songs(uow: UnitOfWork, user: dto.UserDTO, **_):
    return {
        "songs": await services.SongServices(uow).get_favorite_songs_by_user(user_dto=user),
    }
