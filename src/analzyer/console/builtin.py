"""
@author: Annarocia
@date: 2025-10-21
@description: 内置命令
@python: 3.14.0 --nogil
@cunimi: L2
"""

from src.analzyer.console.base import Command
from src.utils.a_logger import Logger
from src.utils.b_config import g_get_config
from src.core_adapters.d_ws_server import g_status_websocket_server, g_is_websocket_server_running, g_stop_websocket_server

logger = Logger("ConsoleAnalzyer", log_level=g_get_config(key="log_level"))

class QuitCmd(Command):
    name = "quit"
    alias = ["exit","stop"]
    description = "退出控制台"
    usage = "quit"
    async def run(self, args: list[str]) -> None:
        raise KeyboardInterrupt # 外层捕获

class HelpCmd(Command):
    name = "help"
    alias = ["?","h"]
    description = "显示帮助信息"
    usage = "help"
    async def run(self, args: list[str]) -> None:
        from src.analzyer.console.router import router
        logger.info(router.help_summary())

class StatusCmd(Command):
    name = "status"
    alias = ["s"]
    description = "显示状态"
    usage = "status"
    async def run(self, args: list[str]) -> None:
        if g_is_websocket_server_running:
            await g_status_websocket_server(await g_is_websocket_server_running())
        logger.info("系统状态: 正在运行")

class StopWSCmd(Command):
    name = "stopws"
    alias = ["stopws"]
    description = "停止WS服务器"
    usage = "stopws"
    async def run(self, args: list[str]) -> None:
        if g_is_websocket_server_running:
            await g_stop_websocket_server()

builtin_commands = [
    QuitCmd,
    HelpCmd,
    StatusCmd,
    StopWSCmd,
]
