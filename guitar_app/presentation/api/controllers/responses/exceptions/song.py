from typing import Any

from pydantic import Field

from guitar_app.presentation.api.controllers.responses.exceptions.base import ApiError


class NotFoundSongError(ApiError):
    detail: Any = Field("Not found song")


class SongIntegrityError(ApiError):
    detail: Any = Field("Ошибка при добавлении песни")
