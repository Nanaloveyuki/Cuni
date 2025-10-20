"""
@author: Annarocia
@date: 2025-10-19
@description: 配置模块
@python: 3.14.0 --nogil
@cunimi: L2
"""

import json
from typing import Any
from ..utils.a_logger import Logger
from os.path import exists

logger = Logger("Config", level="debug")
configs: dict[str, Any] = {
    "host": "localhost",
    "port": 8765,
    "max_cpu_workers": 4,
}
logger.trace("配置模块初始化")
DEFAULT_CONFIG_PATH: str = "./settings.json" 

def g_init_config(*, file_path: str = DEFAULT_CONFIG_PATH) -> bool:
    """
    初始化配置文件
    """
    if exists(file_path):
        logger.debug(f"配置文件 {file_path} 已存在")
        return True
    else:
        try:
            with open(file_path, "w") as f:
                json.dump(configs, f, indent=4)
                logger.debug(f"初始化配置文件 {file_path} 成功")
                return True
        except Exception as e:
            logger.error(f"初始化配置文件失败: {e}")
            return False


def g_get_config(*, file_path: str = DEFAULT_CONFIG_PATH, key: str | None = None) -> Any:
    """
    获取配置
    """
    logger.trace(f"获取配置 {key} 从 {file_path}")
    if exists(file_path):
        logger.trace(f"配置文件 {file_path} 存在")
        try:
            with open(file_path, "r") as f:
                config = json.load(f)
                logger.debug(f"加载配置文件 {file_path} 成功")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return None
    else:
        logger.error(f"配置文件 {file_path} 不存在")
        g_init_config()
        logger.info(f"初始化配置文件 {file_path} 成功")
        return g_get_config(file_path=file_path, key=key)
    if key is None:
        logger.debug(f"配置项Key: {key} 为空")
        return config
    else:
        return config.get(key)

def g_set_config(*, key: str, value: Any, file_path: str = DEFAULT_CONFIG_PATH) -> bool:
    """
    设置配置
    """
    if exists(file_path):
        try:
            with open(file_path, "r") as f:
                config = json.load(f)
                logger.debug(f"加载配置文件 {file_path} 成功")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return False
    config[key] = value
    try:
        with open(file_path, "w") as f:
            json.dump(config, f, indent=4)
            logger.debug(f"设置配置项 {key} 为 {value} 成功")
    except Exception as e:
        logger.error(f"设置配置项 {key} 为 {value} 失败: {e}")
        return False
    return True
