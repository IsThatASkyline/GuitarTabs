from guitar_app.application.common.exceptions import AppException


class MusicianException(AppException):
    """Base musician exception"""

    pass


class MusicianNotExists(MusicianException):
    """Musician not exists error"""

    pass


class SmthWithAddingToBand(MusicianException):
    """Musician not exists error"""

    pass
