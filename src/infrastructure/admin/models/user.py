from sqladmin import ModelView
from src.infrastructure.db.models import User



class UserAdmin(ModelView, model=User):  # type: ignore
    column_list = [
        User.id,
        User.username,
        User.email,
        User.password,
    ]