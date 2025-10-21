"""
@author: Annarocia
@date: 2025-10-19
@description: ws模块 - 正向WebSocket服务器
@python: 3.14.0 --nogil
@cunimi: L2
"""

import asyncio
import websockets
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from src.core.c_asyncio import schedule

# 条件导入
try:
    from ..utils.a_logger import Logger
    from ..utils.b_config import g_get_config
    from ..core.c_asyncio import async_input_queue, async_output_queue
except ImportError:
    raise ImportError("未找到必须的包,请确保包导入正确")

logger = Logger("WebSocket", level=g_get_config(key="log_level"))
is_websocket_server_running: bool = False

# WebSocket服务器配置
WS_HOST: str = g_get_config(key="host") or "localhost"
WS_PORT: int = g_get_config(key="port") or 8765
MAX_CPU_WORKERS: int = g_get_config(key="max_cpu_workers") or 4

Q_OUT = asyncio.Queue()
CPU_POOL = ThreadPoolExecutor(max_workers=MAX_CPU_WORKERS)
PROC_POOL = ProcessPoolExecutor(max_workers=MAX_CPU_WORKERS)

active_clients: set[websockets.WebSocketServerProtocol] = set()

# Recv
async def _recv(websocket: websockets.WebSocketServerProtocol):
    active_clients.add(websocket)
    try:
        async for message in websocket:
            logger.info(f"从 {websocket.remote_address} | 收到消息: {message}")
            await async_input_queue.put(message)
            logger.trace(f"已将消息放入输入队列: {message}")
    finally:
        active_clients.discard(websocket)
        logger.info(f"已移除 {websocket.remote_address} 客户端")

async def _send():
    while True:
        result = await async_output_queue.get()
        dead: tuple = set()
        logger.debug(f"当前活跃客户端数: {len(active_clients)}, 待发送消息: {result}")
        for client in active_clients:
            try:
                await client.send(result)
                logger.info(f"给 {client.remote_address} | 发送消息: {result}")
            except websockets.exceptions.ConnectionClosedOK:
                dead.add(client)
                logger.info(f"客户端 {client.remote_address} 已关闭连接")
        active_clients.difference_update(dead)

async def g_start_websocket_server() -> bool:
    """
    启动WebSocket服务器
    """
    asyncio.create_task(_send())
    asyncio.create_task(schedule())

    await websockets.serve(_recv, WS_HOST, WS_PORT)

    logger.info(f"WS服务器已启动, 监听 {WS_HOST}:{WS_PORT}")
    logger.info(f"当前最大线(进)程数: {MAX_CPU_WORKERS}")
    is_websocket_server_running = True
    await g_status_websocket_server(is_running=is_websocket_server_running)
    logger.debug("等待所有消息发送完成")

    logger.debug("所有消息发送完成")
    return True

async def g_status_websocket_server(is_running: bool) -> bool:
    """
    获取WebSocket服务器状态
    """
    if not is_running:
        logger.warning("WebSocket 服务器未运行")
        return False
    logger.info(f"当前活跃客户端数: {len(active_clients)}")
    logger.info(f"当前待发送消息数: {async_output_queue.qsize()}")
    logger.info(f"当前待处理输入消息数: {async_input_queue.qsize()}")
    logger.info(f"当前待处理输出消息数: {async_output_queue.qsize()}")
    return True

async def g_is_websocket_server_running() -> bool:
    """
    检查WebSocket服务器是否正在运行
    """
    await g_status_websocket_server(is_running=is_websocket_server_running)
    logger.debug(f"当前WebSocket服务器运行状态: {is_websocket_server_running}")
    return is_websocket_server_running

async def g_stop_websocket_server() -> bool:
    """
    停止WebSocket服务器
    """
    if not await g_is_websocket_server_running():
        logger.warning("WebSocket 服务器未运行")
        return False
    logger.info("正在关闭所有活跃客户端连接")
    for client in active_clients:
        await client.close()
    logger.info("所有活跃客户端连接已关闭")
    

    # todo: 关闭服务端
    is_websocket_server_running = False
    await g_status_websocket_server(is_running=is_websocket_server_running)

    logger.info("WebSocket 服务器已停止")
    return True