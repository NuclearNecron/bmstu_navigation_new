import asyncio
import threading
from typing import Callable, Any


class Synchronizer:
    """
    Класс для синхронного выполнения операций.
    Обеспечивает, что только одна операция выполняется в каждый момент времени.
    """

    def __init__(self):
        self._lock = threading.Lock()

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Выполнить функцию синхронно с блокировкой.

        Args:
            func: Функция для выполнения
            *args: Позиционные аргументы
            **kwargs: Именованные аргументы

        Returns:
            Результат выполнения функции

        Raises:
            Любое исключение, которое может выбросить функция
        """
        with self._lock:
            return func(*args, **kwargs)

    async def execute_async(self, func: Callable, *args, **kwargs) -> Any:
        """
        Асинхронная обертка для выполнения функции синхронно.
        Использует asyncio.to_thread для выполнения в отдельном потоке,
        но с блокировкой, обеспечивая последовательность операций.
        """
        return await asyncio.to_thread(self.execute, func, *args, **kwargs)
