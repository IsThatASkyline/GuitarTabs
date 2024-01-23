import pytest

from guitar_app.application.guitar.domain.services.modulation import (
    get_modulated_verses,
)


@pytest.mark.asyncio
async def test_get_modulated_verses(
    modulation_in_data,
    modulation_expected_data,
    modulation_in_data2,
    modulation_expected_data2,
) -> None:
    result = await get_modulated_verses(*modulation_in_data)
    result2 = await get_modulated_verses(*modulation_in_data2)

    assert result == modulation_expected_data
    assert result2 == modulation_expected_data2
