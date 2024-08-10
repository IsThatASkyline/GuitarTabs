from aiogram import F
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format

from ... import states
from .getters import get_all_bands
from .handlers import select_band

all_bands = Dialog(
    Window(
        Const("🎸Все группы"),
        ScrollingGroup(
            Select(
                Format("{item.title}"),
                id="bands",
                item_id_getter=lambda x: x.id,
                items="bands",
                on_click=select_band,
            ),
            id="bands_sg",
            width=2,
            height=7,
            when=F["bands"],
        ),
        Cancel(Const("🔙Назад")),
        state=states.AllBandsPanelSG.choose_band,
        getter=get_all_bands,
    ),
)
