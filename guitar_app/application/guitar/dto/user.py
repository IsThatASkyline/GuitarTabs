from dataclasses import dataclass


@dataclass
class BaseUserDTO:
    telegram_id: int
    id: int | None = None
    username: str | None = None
    is_bot: bool = False
    first_name: str | None = None
    last_name: str | None = None


@dataclass
class CreateUserDTO(BaseUserDTO):
    pass


@dataclass
class UserDTO(BaseUserDTO):
    pass


@dataclass
class UpdateUserDTO(UserDTO):
    pass
