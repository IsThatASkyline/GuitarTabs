from guitar_app.application.guitar import dto

PREVIEW_SONG = dto.SongDTO(
    id=1,
    title="song name",
    band=dto.BandDTO(
        id=1,
        title="band name",
    ),
)
