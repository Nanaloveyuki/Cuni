"""
@author: Annarocia
@date: 2025-10-21
@description: 日志模块
@python: 3.14.0 --nogil
@cunimi: L2
"""

from threading import current_thread
from typing import Any, Mapping, Optional
from dataclasses import dataclass, field
from types import MappingProxyType

from src.utils.a_time import g_get_time

try:
    from . import g_colorize
except ImportError:
    try:
        from a_colorize import g_colorize
    except ImportError:
        def g_colorize(text: str, **kwargs) -> str:
            return text

@dataclass(frozen=True,slots=True)
class LoggerLevel:
    """不可变日志级别"""
    _level_map: Mapping[str, int] = field(init=False)

    def __post_init__(self) -> None:
        """初始化日志级别映射"""
        raw = {
            "unknown": -1,
            "tip": 0,
            "trace": 10,
            "debug": 20,
            "info": 30,
            "warn": 40,
            "error": 50,
            "fatal": 60,
        }
        object.__setattr__(self, "_level_map", MappingProxyType(raw))

    @property
    def level_map(self) -> Mapping[str, int]:
        """日志级别映射"""
        return self._level_map

@dataclass(frozen=True,slots=True)
class LoggerColor:
    """不可变日志颜色"""
    tip: str = "#7392ff"
    trace: str = "#caf3ff"
    debug: str = "#7392ff"
    info: str = "#e8daef"
    warn: str = "#f4cd87"
    error: str = "#ff8863"
    fatal: str = "#ff4141"
    unknown: str = "#ffffff"
    name_color: str = "#bb8fce"
    time_color: str = "#82e0aa"


class Logger:
    """
    日志记录器
    
    Args:
        logger_name (str): 日志记录器名称
        log_level (int): 默认日志级别
        level (Optional[str]): 日志级别字符串，若指定则覆盖默认级别
    
    Statics:
        unknown:-1;
        tip:0;
        trace:10;
        debug:20;
        info:30;
        warn:40;
        error:50;
        fatal:60; 
    """
    def __init__(self, logger_name: str = "", log_level: int = 10, level: Optional[str] = None):
        self.name: str = logger_name
        self.colors = LoggerColor()
        self.level_name_map: list[str]= []
        for key in LoggerLevel().level_map.keys():
            self.level_name_map.append(key)
        self.level_map: Mapping[str, int] = LoggerLevel().level_map
        
        def _norm(lvl):
            if isinstance(lvl, int):
                return lvl
            if isinstance(lvl, str) and lvl in self.level_map:
                return self.level_map[lvl]
            return self.level_map["debug"]  # 默认

        self.level: int = _norm(level if level is not None else log_level)

    def _format_msg(self, msg: Any, current_level: str, no_color: bool) -> str:
        """格式化日志消息"""
        now_thread: str = ""
        if no_color:
            return f"{self.name} {g_get_time("%H:%M:%S.%f")} [{current_level}] {msg}"
        else:
            if hasattr(self.colors, current_level):
                if current_level == "trace":
                    now_thread: str = f":{g_colorize(f"{current_thread().name}", foreground=getattr(self.colors, "name_color"))}"
                front_part: str = f"{g_colorize(f"{self.name}", foreground=getattr(self.colors, "name_color"))}"
                middle_part: str = f"{g_colorize(f"[{current_level}]", foreground=getattr(self.colors, current_level))}"
                time_part: str = f"{g_colorize(f"{g_get_time("%H:%M:%S.%f")}", foreground=getattr(self.colors, "time_color"))}"
                # todo msg正则表达+颜色格式化
                return f"{front_part}{now_thread} {time_part} {middle_part} >> {msg}"
            else:
                return g_colorize(f"{self.name}{now_thread} {g_get_time("%H:%M:%S.%f")} [{current_level}] {msg}", foreground=self.colors.unknown)

    def _print_msg(self, msg: str) -> None:
        print(msg)

    def trace(self, msg: str, no_color: bool = False):
        """打印跟踪级别的日志消息"""
        if self.level <= self.level_map["trace"]:
            self._print_msg(self._format_msg(msg=msg, current_level="trace", no_color=no_color))
        else:
            pass

    def debug(self, msg: str, no_color: bool = False):
        """打印调试级别的日志消息"""
        if self.level <= self.level_map["debug"]:
            self._print_msg(self._format_msg(msg=msg, current_level="debug", no_color=no_color))
        else:
            pass

    def info(self, msg: str, no_color: bool = False):
        """打印信息级别的日志消息"""
        if self.level <= self.level_map["info"]:
            self._print_msg(self._format_msg(msg=msg, current_level="info", no_color=no_color))
        else:
            pass

    def warn(self, msg: str, no_color: bool = False):
        """打印警告级别的日志消息"""
        if self.level <= self.level_map["warn"]:
            self._print_msg(self._format_msg(msg=msg, current_level="warn", no_color=no_color))
        else:
            pass

    def error(self, msg: str, no_color: bool = False):
        """打印错误级别的日志消息"""
        if self.level <= self.level_map["error"]:
            self._print_msg(self._format_msg(msg=msg, current_level="error", no_color=no_color))
        else:
            pass

    def fatal(self, msg: str, no_color: bool = False):
        """打印致命错误级别的日志消息"""
        if self.level <= self.level_map["fatal"]:
            self._print_msg(self._format_msg(msg=msg, current_level="fatal", no_color=no_color))
        else:
            pass

    def tip(self, msg: str, no_color: bool = False):
        """打印提示级别的日志消息"""
        if self.level <= self.level_map["tip"]:
            self._print_msg(self._format_msg(msg=msg, current_level="tip", no_color=no_color))
        else:
            pass
