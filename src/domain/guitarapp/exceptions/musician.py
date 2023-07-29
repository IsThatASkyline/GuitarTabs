from guitar_app.src.domain.common.exceptions import AppException


class MusicianException(AppException):
    """Base musician exception"""

    pass


class MusicianNotExists(MusicianException):
    """Musician not exists error"""

    pass