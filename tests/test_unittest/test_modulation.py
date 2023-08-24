import pytest
from src.domain.guitarapp.utils.modulation import get_modulate_verses


@pytest.mark.asyncio
async def test_get_modulate_verses(
    modulation_in_data,
    modulation_expected_data,
    modulation_in_data2,
    modulation_expected_data2
) -> None:
    result = get_modulate_verses(*modulation_in_data)
    result2 = get_modulate_verses(*modulation_in_data2)

    assert result == modulation_expected_data
    assert result2 == modulation_expected_data2
