"""
@author: Annarocia
@date: 2025-10-20
@description: 服务选择
@python: 3.14.0 --nogil
@cunimi: L2
"""

from src.utils.b_config import g_get_config
from src.utils.a_logger import Logger
from src.utils.a_colorize import g_colorize
from src.core_adapters.d_console import console

adapters: list[str] = [
    "websocket",
]

logger = Logger("Main", level=g_get_config(key="log_level"))

async def g_run():
    """
    运行服务
    """
    selected: bool = False
    while selected is not True:
        logger.info("有如下适配器可选:")
        for listed_adapter in adapters: 
            logger.info(f" |  {listed_adapter}")

        logger.info("请输入适配器名称: ")
        try:
            adapter = input(g_colorize(" >>> ", foreground="#bb8fce"))
        except KeyboardInterrupt:
            logger.info("用户终止进程")
            break
        except EOFError:
            logger.info("用户终止进程")
            break
        except Exception as e:
            logger.error(f"输入适配器时发生错误: {e}")
            continue
        logger.info(f"你选择了适配器: {adapter}")
        if adapter not in adapters:
            logger.error(f"适配器 {adapter} 不存在")
            continue
        
        if adapter == "websocket":
            from src.core_adapters.d_ws_server import g_start_websocket_server
            if await g_start_websocket_server():
                logger.info("WebSocket 服务器已在后台启动")
            else:
                logger.error("WebSocket 服务器启动失败")
        try:
            await console()
            selected: bool = True
        except KeyboardInterrupt:
            logger.info("控制台已退出")
            return
