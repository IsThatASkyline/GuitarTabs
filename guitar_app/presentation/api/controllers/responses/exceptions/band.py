from typing import Any

from pydantic import Field

from guitar_app.presentation.api.controllers.responses.exceptions.base import ApiError


class NotFoundBandError(ApiError):
    detail: Any = Field("Not found band")
