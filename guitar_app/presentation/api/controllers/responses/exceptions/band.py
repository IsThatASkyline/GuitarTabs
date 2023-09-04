from pydantic import Field

from guitar_app.presentation.api.controllers.responses.exceptions.base import ApiError


class NotFoundBandError(ApiError):
    detail = Field("Not found band", const=True)
