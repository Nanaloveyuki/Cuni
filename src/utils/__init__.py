"""
@author: Annarocia
@date: 2025-10-19
@description: 工具包
@python: 3.14.0 --nogil
@cunimi: L2
"""
__version__: str = "1.0.0"

from .a_colorize import g_colorize, g_get_terminal_compatible_color
from .a_logger import Logger
from .a_time import g_get_time
from .b_config import g_get_config, g_init_config, g_set_config

__all__: list[str] = [
    "g_colorize",
    "g_get_terminal_compatible_color",
    "Logger",
    "g_get_time",
    "g_get_config",
    "g_init_config",
    "g_set_config"
]