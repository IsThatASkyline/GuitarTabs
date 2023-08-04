from sqladmin import ModelView
from src.infrastructure.db.models import Musician


class MusicianAdmin(ModelView, model=Musician):  # type: ignore
    column_list = [
        Musician.id,
        Musician.first_name,
        Musician.last_name,
    ]
