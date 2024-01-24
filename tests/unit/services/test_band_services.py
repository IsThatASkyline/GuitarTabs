import pytest

from guitar_app.application.guitar.dto import CreateBandDTO, BandDTO
from guitar_app.application.guitar.exceptions import BandNotExists
from guitar_app.application.guitar.services import BandServices
from tests.mocks.repo import FakeUnitOfWork, FakeBandRepo


@pytest.mark.asyncio
async def test_create_band_service():
    band_data = CreateBandDTO(title='The Smiths')
    band = await BandServices(uow=FakeUnitOfWork()).create_band(band_data)
    assert band.title == band_data.title


@pytest.mark.asyncio
async def test_get_all_bands_service():
    band_data_1 = BandDTO(id=1, title='The Smiths')
    band_data_2 = BandDTO(id=2, title='Muse')
    repo = FakeBandRepo([band_data_1, band_data_2])
    bands = await BandServices(uow=FakeUnitOfWork(band_repo=repo)).get_all_bands()
    assert len(bands) == 2
    assert bands[0].title == band_data_1.title
    assert bands[1].title == band_data_2.title


@pytest.mark.asyncio
async def test_get_band_by_id_service():
    band_data_1 = BandDTO(id=1, title='The Smiths')
    band_data_2 = BandDTO(id=2, title='Muse')
    repo = FakeBandRepo([band_data_1, band_data_2])
    band = await BandServices(uow=FakeUnitOfWork(band_repo=repo)).get_band_by_id(2)
    assert band.title == band_data_2.title
    with pytest.raises(BandNotExists):
        await BandServices(uow=FakeUnitOfWork(band_repo=repo)).get_band_by_id(100)


@pytest.mark.asyncio
async def test_delete_band_service():
    band_data_1 = BandDTO(id=1, title='The Smiths')
    band_data_2 = BandDTO(id=2, title='Muse')
    repo = FakeBandRepo([band_data_1, band_data_2])
    await BandServices(uow=FakeUnitOfWork(band_repo=repo)).delete_band(2)
    with pytest.raises(BandNotExists):
        await BandServices(uow=FakeUnitOfWork(band_repo=repo)).get_band_by_id(2)

