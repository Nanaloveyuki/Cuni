"""
@author: Annarocia
@date: 2025-10-19
@description: 测试WS模块 -- 反向WebSocket客户端
@python: 3.14.0 --nogil
@cunimi: L2
"""

import asyncio
import json
import websockets
from concurrent.futures import ThreadPoolExecutor

# 使用正确的导入路径
try:
    from src.utils.a_logger import Logger
except ImportError:
    # 如果直接运行测试文件，尝试从相对路径导入
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.utils.a_logger import Logger

logger = Logger(level="trace", logger_name="WSClient")

# WebSocket服务器地址
URL: str = "ws://localhost:8765"

executor = ThreadPoolExecutor(max_workers=1)

# -------------- 控制台输入（异步化）--------------
async def ainput(prompt: str = "> ") -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, input, prompt)

# -------------- 接收任务 --------------
async def recv_task(ws: websockets.WebSocketClientProtocol):
    async for msg in ws:
        try:
            data = json.loads(msg)
            logger.info(f"Server > {data}")
        except json.JSONDecodeError:
            logger.info(f"Server > {msg}")

# -------------- 发送任务 --------------
async def send_task(ws: websockets.WebSocketClientProtocol):
    while True:
        line = await ainput()
        if line.strip() == "/quit":
            logger.info("Bye~")
            await ws.close()
            break
        if line.strip() == "atk":
            times: int = int(await ainput("Attack times: "))
            for i in range(times + 1):
                await ws.send(f"测试攻击次数 {i}")
        await ws.send(line.strip())

# -------------- 主流程 --------------
async def main():
    logger.info(f"Connecting to {URL} ...")
    async with websockets.connect(URL) as ws:
        logger.info("Connected! Type /quit to exit.")
        logger.info("Type 'atk' to attack n times.")
        # 并发跑：收 + 发
        await asyncio.gather(recv_task(ws), send_task(ws))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Client interrupted.")