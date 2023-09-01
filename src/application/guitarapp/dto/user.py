from pydantic.main import BaseModel


class BaseUserDTO(BaseModel):
    telegram_id: int

    class Config:
        orm_mode = True


class CreateUserDTO(BaseUserDTO):
    pass


class UserDTO(BaseUserDTO):
    pass


class UpdateUserDTO(UserDTO):
    pass
