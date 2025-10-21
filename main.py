"""
@author: Annarocia
@date: 2025-10-19
@description: 启动程序
@python: 3.14.0 --nogil
@cunimi: L2
"""

from src.core_adapters.d_service_select import g_run
from src.utils.a_logger import Logger
import asyncio

logger = Logger("Main")
logger.info("Bonjour Cunimi! Bonjour Liteyuki!")

async def main():
    await g_run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("适配器已被用户终止进程")
    finally:
        logger.info("SEE YOU AGAIN~")