"""
@author: Annarocia
@date: 2025-10-19
@description: 项目入口
@python: 3.14.0 --nogil
@cunimi: L2
"""

__version__: str = "1.0.0"

from .utils import Logger, g_colorize, g_get_terminal_compatible_color
from .core_adapters import g_start_websocket_server, g_run

__all__: list[str] = [
    "g_colorize",
    "g_get_terminal_compatible_color",
    "Logger",
    "g_start_websocket_server",
    "g_run",
]