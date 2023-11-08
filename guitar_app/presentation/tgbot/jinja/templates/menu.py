from aiogram import F
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.text import Const, Format

from guitar_app.presentation.tgbot.dialogs.song_manage.handlers import down_key, up_key

modulation_menu = Row(
    Button(
        Const("⬇"),
        id="key_minus",
        on_click=down_key,
    ),
    Button(
        Format("Тональность"),
        id="modulation_value",
        when=F["mod_value"] == 0,
    ),
    Button(
        Format("+{mod_value}"),
        id="modulation_value",
        when=F["mod_value"] > 0,
    ),
    Button(
        Format("{mod_value}"),
        id="modulation_value",
        when=F["mod_value"] < 0,
    ),
    Button(
        Const("⬆"),
        id="key_plus",
        on_click=up_key,
    )
)
