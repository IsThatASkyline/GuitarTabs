from sqladmin import Admin


from guitar_app.src.infrastructure.admin.models.musician import MusicianAdmin
from guitar_app.src.infrastructure.admin.models.user import UserAdmin


def setup_admin_models(admin_app: Admin) -> None:
    for app in [MusicianAdmin, UserAdmin]:
        admin_app.add_view(app)
