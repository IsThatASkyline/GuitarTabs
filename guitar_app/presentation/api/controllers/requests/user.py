from pydantic.main import BaseModel


class BaseUser(BaseModel):
    telegram_id: int


class CreateUserRequest(BaseUser):
    pass


class UpdateUserRequest(BaseUser):
    pass
