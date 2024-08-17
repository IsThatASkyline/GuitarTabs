from typing import Any

from pydantic import Field

from guitar_app.presentation.api.controllers.responses.exceptions.base import ApiError


class NotFoundUserError(ApiError):
    detail: Any = Field("Not found user")
