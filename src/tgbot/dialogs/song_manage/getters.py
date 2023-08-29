from src.infrastructure.db.uow import UnitOfWork
from src.application.guitarapp import services

async def get_song(**_):
    return {
        "title": "song_name",
        "band": "band_name"
    }


async def get_all_songs(uow: UnitOfWork, **_):
    return {
        "songs": await services.SongServices(uow).get_all_songs()
    }


async def get_songs_by_band(**_):
    return {
        "songs": [
            {
                "id": 1,
                "title": "bandsong1",
            },
            {
                "id": 2,
                "title": "bandsong2",
            },
            {
                "id": 3,
                "title": "bandsong3",
            },
        ],
    }


async def get_favorite_songs(**_):
    return {
        "songs": [
            {
                "id": 1,
                "title": "favsong1",
            },
            {
                "id": 2,
                "title": "favsong2",
            },
        ],
    }


async def get_chords(**_):
    return {
        "title": "Звезда по имени Солнце",
        "chords": "Am C Dm G",
    }

