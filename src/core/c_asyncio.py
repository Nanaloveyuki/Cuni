"""
@author: Annarocia
@date: 2025-10-19
@description: 异步管理模块
@python: 3.14.0 --nogil
@cunimi: L2
"""

import asyncio
from ..utils.a_logger import Logger
from ..utils.b_config import g_get_config
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

logger = Logger("AsyncioManager", level=g_get_config(key="log_level"))

async_input_queue: asyncio.Queue[str] = asyncio.Queue()
async_output_queue: asyncio.Queue[str] = asyncio.Queue()

if g_get_config(key="use_process_pool"):
    thread_pool = ProcessPoolExecutor(max_workers=g_get_config(key="max_cpu_workers")) or 4
else:
    thread_pool = ThreadPoolExecutor(max_workers=g_get_config(key="max_cpu_workers")) or 4

async def schedule():
    loop = asyncio.get_running_loop()
    while True:
        if async_input_queue.qsize() > g_get_config(key="max_input_queue_size"):
            logger.warning("输入队列已满,消息被丢弃")
            continue
        msg = await async_output_queue.get()
        logger.trace(f"调度器收到消息: {msg}")
        from src.analzyer.e_analzyer import g_msg_analyzer
        future = loop.run_in_executor(thread_pool, g_msg_analyzer, msg, "console")
        result = await future
        logger.trace(f"调度器分析结果: {result}")
        if result:
            await async_output_queue.put(result)
        else:
            logger.debug("分析器返回空结果,消息被丢弃")


