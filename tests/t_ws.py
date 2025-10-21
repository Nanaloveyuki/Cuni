"""
@author: Annarocia
@date: 2025-10-19
@description: 测试WS模块
@python: 3.14.0 --nogil
@cunimi: L2
"""

# 使用正确的导入路径
import asyncio
try:
    from src.utils.a_logger import Logger
    from src.core_adapters.d_service_select import g_run
except ImportError:
    # 如果直接运行测试文件，尝试从相对路径导入
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.utils.a_logger import Logger
    from src.core_adapters.d_service_select import g_run

logger = Logger(level="trace", logger_name="Tests")

logger.info("测试WS模块")

if __name__ == "__main__":
    try:
        asyncio.run(g_run())
    except KeyboardInterrupt:
        logger.info("WS服务器测试结束")
    finally:
        logger.info("SEE YOU AGAIN!")