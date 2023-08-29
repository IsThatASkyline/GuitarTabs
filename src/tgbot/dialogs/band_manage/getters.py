
async def get_song(**_):
    return {
        "title": "song_name",
        "band": "band_name"
    }

async def get_band(**_):
    return {
        "title": "band_name",
    }


async def get_all_bands(**_):
    return {
        "bands": [
            {
                "id": 1,
                "title": "band1",
            },
            {
                "id": 2,
                "title": "band2",
            },
            {
                "id": 3,
                "title": "band3",
            },
        ],
    }