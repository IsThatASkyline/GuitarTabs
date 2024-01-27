import pytest

from guitar_app.application.guitar.dto import (
    BandDTO,
    CreateSongDTO,
    GetSongDTO,
    SongDTO,
)
from guitar_app.application.guitar.exceptions import SongNotExists
from guitar_app.application.guitar.services import SongServices
from tests.mocks.repo import FakeSongRepo, FakeUnitOfWork


@pytest.mark.asyncio
async def test_create_song_service():
    song_data = CreateSongDTO(title="Bigmouth Strikes Again", band_id=1)
    song = await SongServices(uow=FakeUnitOfWork()).create_song(song_data)
    assert song.title == song_data.title


@pytest.mark.asyncio
async def test_get_all_songs_service():
    song_data_1 = SongDTO(
        id=1, title="Bigmouth Strikes Again", band=BandDTO(id=1, title="The Smiths")
    )
    song_data_2 = SongDTO(id=2, title="This Charming Man", band=BandDTO(id=1, title="The Smiths"))
    repo = FakeSongRepo([song_data_1, song_data_2])
    songs = await SongServices(uow=FakeUnitOfWork(song_repo=repo)).get_all_songs()
    assert len(songs) == 2
    assert songs[0].title == song_data_1.title
    assert songs[1].title == song_data_2.title


@pytest.mark.asyncio
async def test_get_song_by_id_service():
    song_data_1 = SongDTO(
        id=1, title="Bigmouth Strikes Again", band=BandDTO(id=1, title="The Smiths")
    )
    song_data_2 = SongDTO(id=2, title="This Charming Man", band=BandDTO(id=1, title="The Smiths"))
    repo = FakeSongRepo([song_data_1, song_data_2])
    song = await SongServices(uow=FakeUnitOfWork(song_repo=repo)).get_song_by_id(
        GetSongDTO(song_id=2)
    )
    assert song.title == song_data_2.title
    with pytest.raises(SongNotExists):
        await SongServices(uow=FakeUnitOfWork(song_repo=repo)).get_song_by_id(
            GetSongDTO(song_id=100)
        )


@pytest.mark.asyncio
async def test_delete_song_service():
    song_data_1 = SongDTO(
        id=1, title="Bigmouth Strikes Again", band=BandDTO(id=1, title="The Smiths")
    )
    song_data_2 = SongDTO(id=2, title="This Charming Man", band=BandDTO(id=1, title="The Smiths"))
    repo = FakeSongRepo([song_data_1, song_data_2])
    await SongServices(uow=FakeUnitOfWork(song_repo=repo)).delete_song(2)
    with pytest.raises(SongNotExists):
        await SongServices(uow=FakeUnitOfWork(song_repo=repo)).get_song_by_id(GetSongDTO(song_id=2))
