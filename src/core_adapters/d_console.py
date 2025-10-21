"""
@author: Annarocia
@date: 2025-10-21
@description: 控制台
@python: 3.14.0 --nogil
@cunimi: L2
"""

from typing import Any
from src.utils.b_config import g_get_config
from src.utils.a_logger import Logger
from src.utils.a_colorize import g_colorize
from src.analzyer.console.router import router

console_logger = Logger("Console", level=g_get_config(key="log_level"))
        
async def console() -> Any:
    """
    控制台
    """
    console_logger.info("控制台已启动")
    console_logger.info("输入 /quit 或 /exit 可退出控制台")
    while True:
        try:
            line = input(g_colorize(" >>> ", foreground="#bb8fce"))
        except KeyboardInterrupt:
            console_logger.info("用户终止进程")
            break
        except EOFError:
            console_logger.info("用户终止进程")
            break
        except Exception as e:
            console_logger.error(f"输入控制台时发生错误: {e}")
            continue

        console_logger.info(f"控制台输入: {line}")

        if line.startswith("/"):
            argv = line[1:].split(maxsplit=1)
            cmd_name = argv[0]
            raw_args = argv[1].split() if len(argv) > 1 else ""
            cmd = router.get(cmd_name)
            if not cmd:
                console_logger.error(f"未知控制台命令: {cmd_name}")
                continue
            try:
                result = await cmd.run(args=raw_args)
                if result:
                    console_logger.info(str(result))
            except Exception as e:
                console_logger.error(f"执行控制台命令时发生错误: {e}")
                continue
        else:
            console_logger.info(f"未识别的控制台输入: {line}")
            continue
