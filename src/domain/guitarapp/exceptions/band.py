from src.domain.common.exceptions import AppException


class BandException(AppException):
    """Base band exception"""

    pass


class BandNotExists(BandException):
    """Band not exists error"""
