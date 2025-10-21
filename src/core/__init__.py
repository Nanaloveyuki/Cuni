"""
@author: Annarocia
@date: 2025-10-19
@description: 核心模块
@python: 3.14.0 --nogil
@cunimi: L2
"""
__version__: str = "1.0.0"

from .c_asyncio import async_input_queue, async_output_queue

__all__: list[str] = [
    "async_input_queue",
    "async_output_queue",
]