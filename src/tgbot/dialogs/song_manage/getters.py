

async def get_song(**_):
    return {
        "title": "song_name",
        "band": "band_name"
    }


async def get_all_songs(**_):
    return {
        "songs": [
            {
                "id": 1,
                "title": "song1",
            },
            {
                "id": 2,
                "title": "song2",
            },
            {
                "id": 3,
                "title": "song3",
            },
        ],
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


async def get_chords(**_):
    return {
        "title": "Звезда по имени Солнце",
        "chords": "Am C Dm G",
    }

