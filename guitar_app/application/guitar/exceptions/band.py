from guitar_app.application.common.exceptions import AppException


class BandException(AppException):
    """Base band exception"""

    pass


class BandNotExists(BandException):
    """Band not exists error"""
