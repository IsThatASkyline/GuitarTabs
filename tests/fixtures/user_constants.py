from aiogram.types import User

from guitar_app.application.guitar import dto

JOHNNY_TG_ID = 121212
JOHNNY_FIRST_NAME = "Johnny"
JOHNNY_LAST_NAME = "Marr"
JOHNNY_NEW_USERNAME = "best_riffs_in_the_world"
JOHNNY_OLD_USERNAME = "the_smiths_guitarist"

JOHNNY_DTO = dto.UserDTO(
    telegram_id=JOHNNY_TG_ID,
    first_name=JOHNNY_FIRST_NAME,
    last_name=JOHNNY_LAST_NAME,
    username=JOHNNY_NEW_USERNAME,
    is_bot=False,
)


def create_tg_user(
    id_: int = JOHNNY_TG_ID,
    username: str = JOHNNY_NEW_USERNAME,
    first_name: str = JOHNNY_FIRST_NAME,
    last_name: str = JOHNNY_LAST_NAME,
) -> User:
    return User(
        id=id_,
        username=username,
        first_name=first_name,
        last_name=last_name,
        is_bot=False,
    )
