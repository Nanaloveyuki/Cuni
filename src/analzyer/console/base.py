"""
@author: Annarocia
@date: 2025-10-21
@description: Base命令类型基类
@python: 3.14.0 --nogil
@cunimi: L2
"""
from abc import ABC, abstractmethod
import shlex
from typing import Any

class Command(ABC):
    """
    命令类型基类
    """
    name: str # 不含 /
    alias: list[str] = []
    description: str
    usage: str

    @abstractmethod
    async def run(self, args: list[str]) -> Any:
        """
        命令运行函数, return打印结果
        """

    async def parse_args(self, msg_str: str) -> Any:
        """
        解析传入内容为参数列表
        :param msg_str: 传入内容
        :return: 参数列表
        """
        return self.run(shlex.split(msg_str))