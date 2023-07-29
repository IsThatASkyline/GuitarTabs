from sqladmin import ModelView

from guitar_app.src.infrastructure.db.models import Musician


class MusicianAdmin(ModelView, model=Post):  # type: ignore
    column_list = [
        Musician.id,
        Musician.first_name,
        Musician.last_name,
    ]
