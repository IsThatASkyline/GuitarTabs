from pydantic.main import BaseModel


class BaseUserDTO(BaseModel):
    id: int | None
    telegram_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None
    is_bot: bool = False

    class Config:
        orm_mode = True


class CreateUserDTO(BaseUserDTO):
    pass


class UserDTO(BaseUserDTO):
    pass


class UpdateUserDTO(UserDTO):
    pass
