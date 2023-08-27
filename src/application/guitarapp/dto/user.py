from pydantic.main import BaseModel


class BaseUserDTO(BaseModel):
    username: str
    email: str
    password: str


class CreateUserDTO(BaseUserDTO):
    pass


class UpdateUserDTO(BaseUserDTO):
    id: int
    username: str | None = None
    email: str | None = None
    password: str | None = None


class UserDTO(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True