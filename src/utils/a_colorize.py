"""
@author: Annarocia
@date: 2025-10-19
@description: 日志模块颜色化
@python: 3.14.0 --nogil
@cunimi: L2
"""

from typing import Tuple, Optional


class ColorFormatError(ValueError):
    """
    颜色格式错误异常类
    当输入的颜色格式不符合要求时抛出
    """
    pass


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    将十六进制颜色字符串转换为RGB元组
    
    Args:
        hex_color (str): 十六进制颜色字符串，支持#RGB、#RGBA、#RRGGBB、#RRGGBBAA格式
        
    Returns:
        Tuple[int, int, int]: RGB颜色值元组 (r, g, b)
        
    Raises:
        ColorFormatError: 当输入的颜色格式不符合要求时
    """
    # 去除可能的前缀
    hex_color = hex_color.lstrip('#')
    
    # 验证输入长度
    valid_lengths = (3, 4, 6, 8)
    if len(hex_color) not in valid_lengths:
        raise ColorFormatError(f"无效的十六进制颜色格式: {hex_color}")
    
    # 转换为RGB
    try:
        # 处理短格式 (#RGB -> #RRGGBB)
        if len(hex_color) in (3, 4):
            hex_color = ''.join([c * 2 for c in hex_color[:3]])
        
        # 提取RGB值
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        return (r, g, b)
    except ValueError as e:
        raise ColorFormatError(f"无效的十六进制颜色值: {hex_color}") from e


def _rgb_to_ansi_256(r: int, g: int, b: int) -> str:
    """
    将RGB颜色转换为ANSI 256色代码
    
    Args:
        r (int): 红色通道值 (0-255)
        g (int): 绿色通道值 (0-255)
        b (int): 蓝色通道值 (0-255)
        
    Returns:
        str: ANSI 256色代码
    """
    # 规范化RGB值到0-5范围
    r = max(0, min(5, r // 51))  # 51 = 255 / 5
    g = max(0, min(5, g // 51))
    b = max(0, min(5, b // 51))
    
    # 计算256色索引
    color_code = 16 + 36 * r + 6 * g + b
    return f"38;5;{color_code}"


def _rgb_to_ansi_truecolor(r: int, g: int, b: int) -> str:
    """
    将RGB颜色转换为ANSI真彩色代码
    
    Args:
        r (int): 红色通道值 (0-255)
        g (int): 绿色通道值 (0-255)
        b (int): 蓝色通道值 (0-255)
        
    Returns:
        str: ANSI真彩色代码
    """
    return f"38;2;{r};{g};{b}"


def g_colorize(text: str, 
              foreground: Optional[str] = None, 
              background: Optional[str] = None, 
              use_truecolor: bool = True) -> str:
    """
    使用ANSI颜色代码为文本添加颜色
    
    Args:
        text (str): 要着色的文本
        foreground (Optional[str]): 前景色的十六进制颜色代码，如 #FF0000
        background (Optional[str]): 背景色的十六进制颜色代码，如 #00FF00
        use_truecolor (bool): 是否使用真彩色模式，默认为True
        
    Returns:
        str: 带有ANSI颜色代码的文本
        
    Raises:
        ColorFormatError: 当输入的颜色格式不符合要求时
    """
    # 选择颜色转换函数
    rgb_to_ansi = _rgb_to_ansi_truecolor if use_truecolor else _rgb_to_ansi_256
    
    # 构建ANSI代码
    ansi_codes = []
    
    if foreground:
        r, g, b = _hex_to_rgb(foreground)
        ansi_codes.append(rgb_to_ansi(r, g, b))
    
    if background:
        r, g, b = _hex_to_rgb(background)
        # 背景色使用48前缀
        ansi_code = rgb_to_ansi(r, g, b)
        ansi_code = ansi_code.replace("38", "48")
        ansi_codes.append(ansi_code)
    
    # 如果没有指定颜色，直接返回原文本
    if not ansi_codes:
        return text
    
    # 组合ANSI代码
    return f"\033[{';'.join(ansi_codes)}m{text}\033[0m"


def g_get_terminal_compatible_color(hex_color: str) -> str:
    """
    获取终端兼容的颜色表示
    
    Args:
        hex_color (str): 十六进制颜色代码
        
    Returns:
        str: 兼容的ANSI颜色代码字符串
        
    Raises:
        ColorFormatError: 当输入的颜色格式不符合要求时
    """
    r, g, b = _hex_to_rgb(hex_color)
    
    # 尝试检测终端是否支持真彩色
    # 注意：这是一个简化的检测方法，实际应用中可能需要更复杂的检测
    try:
        import os
        term = os.environ.get('TERM', '')
        supports_truecolor = ('256color' in term or 'truecolor' in term)
        rgb_to_ansi = _rgb_to_ansi_truecolor if supports_truecolor else _rgb_to_ansi_256
        return rgb_to_ansi(r, g, b)
    except Exception:
        # 发生异常时默认使用256色
        return _rgb_to_ansi_256(r, g, b)