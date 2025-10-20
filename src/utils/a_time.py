"""
@author: Annarocia
@date: 2025-10-19
@description: 时间模块
@python: 3.14.0 --nogil
@cunimi: L2
"""

from datetime import datetime

def g_get_time(time_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间
    :param time_format: 时间格式
    :return: 格式化后的时间字符串
    """
    return datetime.now().strftime(time_format)
