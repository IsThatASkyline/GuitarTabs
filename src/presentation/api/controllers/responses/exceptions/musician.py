from pydantic import Field
from src.presentation.api.controllers.responses.exceptions.base import ApiError


class NotFoundMusicianError(ApiError):
    detail = Field("Not found musician", const=True)


class MusicianToBandIntegrityError(ApiError):
    detail = Field("Ошибка при добавлении музыканта в группу", const=True)
