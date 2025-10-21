"""
@author: Annarocia
@date: 2025-10-21
@description: 分析总成
@python: 3.14.0 --nogil
@cunimi: L2
"""

from typing import Any
from src.utils.a_logger import Logger
from src.utils.b_config import g_get_config
from src.analzyer.e_ws_analzyer import g_ws_analyzer
from src.analzyer.console.router import router

logger = Logger("MsgAnalyzer", level=g_get_config(key="log_level"))

def g_msg_analyzer(msg_str: Any, msg_from: str) -> Any:
    """
    解析传入字符串
    """
    if msg_from == "console":
        cmd = router.get(msg_str)
        if not cmd:
            logger.error(f"未知控制台命令: {msg_str}")
            return None
        return cmd.execute(msg_str)
    elif msg_from == "ws":
        return g_ws_analyzer(msg_str)
    else:
        logger.error(f"未知消息来源: {msg_from}")
    return None


