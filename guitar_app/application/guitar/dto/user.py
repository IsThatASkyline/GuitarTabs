from pydantic.main import BaseModel


class BaseUserDTO(BaseModel):
    id: int | None
    telegram_id: int
    username: str | None

    class Config:
        orm_mode = True


class CreateUserDTO(BaseUserDTO):
    pass


class UserDTO(BaseUserDTO):
    pass


class UpdateUserDTO(UserDTO):
    pass
