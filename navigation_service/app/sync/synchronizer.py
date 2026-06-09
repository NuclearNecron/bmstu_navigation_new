# navigation_service/app/sync/synchronizer.py
import asyncio
from typing import Callable, Any, Union
import inspect

class Synchronizer:
    def __init__(self):
        self._lock = asyncio.Lock()  # Use async lock for async operations

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        # Only for sync functions
        # Not used if all methods are async — can be removed or kept for hybrid
        return func(*args, **kwargs)

    async def execute_async(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute async func under lock to serialize operations.
        func must be a coroutine function (async def).
        """
        async with self._lock:
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                # Fallback: sync func → run in thread
                loop = asyncio.get_running_loop()
                return await loop.run_in_executor(None, lambda: func(*args, **kwargs))