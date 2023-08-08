import pytest

from src.application.services.modulation import get_modulate_verses


@pytest.mark.asyncio
async def test_get_modulate_verses(
    in_data,
    expected_data,
    in_data2,
    expected_data2
) -> None:
    result = get_modulate_verses(*in_data)
    result2 = get_modulate_verses(*in_data2)

    assert result == expected_data
    assert result2 == expected_data2
