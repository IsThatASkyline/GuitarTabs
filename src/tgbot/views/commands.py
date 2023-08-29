from dataclasses import dataclass

from aiogram.types import BotCommand


@dataclass
class CommandsGroup:
    group_name: str
    commands: list[BotCommand]

    def __str__(self):
        return f"{self.group_name}\n" + "\n".join(
            map(lambda x: f"/{x.command} - {x.description}", self.commands)
        )


START_COMMAND = BotCommand(command="start", description="начало работы с ботом")
HELP_COMMAND = BotCommand(command="help", description="помощь")
CANCEL_COMMAND = BotCommand(command="cancel", description="отмена начатого диалога")

HELP_BASE = CommandsGroup(
    "Базовые команды:",
    [
        START_COMMAND,
        HELP_COMMAND,
        CANCEL_COMMAND,
    ],
)

DEFAULT_COMMANDS = [
    HELP_COMMAND,
    CANCEL_COMMAND,
]