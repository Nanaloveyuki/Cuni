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
except ImportError:
    # 如果直接运行测试文件，尝试从相对路径导入
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.utils.a_logger import Logger

logger = Logger(level="trace",logger_name="Tests")

# no color
logger.trace("test trace running", no_color=True)
logger.debug("test debug running", no_color=True)
logger.info("test info running", no_color=True)
logger.warn("test warn running", no_color=True)
logger.error("test error running", no_color=True)
logger.fatal("test fatal running", no_color=True)
logger.tip("test tip running", no_color=True)

# colorized
logger.trace("test trace running")
logger.debug("test debug running")
logger.info("test info running")
logger.warn("test warn running")
logger.error("test error running")
logger.fatal("test fatal running")
logger.tip("test tip running")

# name
logger2 = Logger("Apps",level="info")
logger2.tip("我已出仓,感觉良好")
logger2.info("我已出仓,感觉良好")
