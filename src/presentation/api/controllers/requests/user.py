from pydantic.main import BaseModel


class BaseUser(BaseModel):
    username: str
    email: str
    password: str


class CreateUserRequest(BaseUser):
    pass


class UpdateUserRequest(BaseUser):
    username: str | None = None
    email: str | None = None
    password: str | None = None