from pydantic import Field

from src.presentation.api.controllers.responses.exceptions.base import ApiError


class NotFoundSongError(ApiError):
    detail = Field("Not found song", const=True)


class SongIntegrityError(ApiError):
    detail = Field("Ошибка при добавлении песни", const=True)
