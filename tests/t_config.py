"""
@author: Annarocia
@date: 2025-10-19
@description: 测试日志模块
@python: 3.14.0 --nogil
@cunimi: L2
"""

# 使用正确的导入路径
try:
    from src.utils.a_logger import Logger
    from src.utils.b_config import g_get_config, g_set_config, g_init_config
except ImportError:
    # 如果直接运行测试文件，尝试从相对路径导入
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.utils.a_logger import Logger
    from src.utils.b_config import g_get_config, g_set_config, g_init_config

logger = Logger(level="trace",logger_name="Tests")

logger.info("测试配置模块")
g_init_config()
logger.info("测试获取配置项")
host = g_get_config(key="host")
logger.info(f"host: {host}")
port = g_get_config(key="port")
logger.info(f"port: {port}")
logger.info("测试设置配置项")
g_set_config(key="host", value="127.0.0.1")
host = g_get_config(key="host")
logger.info(f"host: {host}")


