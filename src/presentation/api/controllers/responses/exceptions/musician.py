from pydantic import Field

from guitar_app.src.presentation.api.controllers.responses.exceptions.base import ApiError


class NotFoundMusicianError(ApiError):
    detail = Field("Not found musician", const=True)