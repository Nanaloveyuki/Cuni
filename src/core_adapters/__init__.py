"""
@author: Annarocia
@date: 2025-10-20
@description: 核心适配器
@python: 3.14.0 --nogil
@cunimi: L2
"""
__version__: str = "1.0.0"

from .d_ws_server import g_start_websocket_server, g_is_websocket_server_running, g_stop_websocket_server
from .d_service_select import g_run

__all__: list[str] = [
    "g_start_websocket_server",
    "g_is_websocket_server_running",
    "g_stop_websocket_server",
    "g_run",
]