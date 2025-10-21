"""
@author: Annarocia
@date: 2025-10-21
@description: 命令全局路由
@python: 3.14.0 --nogil
@cunimi: L2
"""

from typing import Optional
from src.analzyer.console.base import Command
from src.utils.a_logger import Logger
from src.utils.b_config import g_get_config

logger = Logger("ConsoleAnalzyer", log_level=g_get_config(key="log_level"))

class Router:
    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}

    def register(self, command: Command) -> None:
        """
        注册命令
        """
        self._commands[command.name, *command.alias] = command
        for alias in command.alias:
            self._commands[alias] = command

    def get(self, name: str) -> Optional[Command]:
        """
        获取命令
        """
        return self._commands.get(name)

    def help_summary(self) -> str:
        lines: list = ["命令列表:"]
        for command in dict.fromkeys(self._commands.values()):
            lines.append(f"| {command.name} - {command.description}")
        return "\n".join(lines)

router = Router()
