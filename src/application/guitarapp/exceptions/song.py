from src.application.common.exceptions import AppException


class SongException(AppException):
    """Base song exception"""

    pass


class SongNotExists(SongException):
    """Song not exists error"""

    pass


class CreateSongException(SongException):
    """Musician not exists error"""

    pass
