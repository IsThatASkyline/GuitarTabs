from abc import ABC

from pydantic import BaseModel


class AbstractDTO(BaseModel, ABC):
    pass
