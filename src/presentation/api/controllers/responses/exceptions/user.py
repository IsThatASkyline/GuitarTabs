from pydantic import Field

from src.presentation.api.controllers.responses.exceptions.base import ApiError


class NotFoundUserError(ApiError):
    detail = Field("Not found user", const=True)