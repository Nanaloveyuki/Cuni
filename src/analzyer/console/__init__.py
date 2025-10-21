"""
@author: Annarocia
@date: 2025-10-21
@description: 控制台命令
@python: 3.14.0 --nogil
@cunimi: L2
"""

from .base import Command
from .router import router
from .builtin import builtin_commands
from src.utils.a_logger import Logger
from src.utils.b_config import g_get_config

logger = Logger("ConsoleAnalzyer", log_level=g_get_config(key="log_level"))


def _auto_register():
    """
    自动注册所有内置命令
    """
    for cmd in builtin_commands:
        router.register(cmd())

_auto_register()

__all__ = [
    "Command",
    "router"
]
