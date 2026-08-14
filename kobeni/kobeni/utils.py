import asyncio
from functools import wraps


def sequential(func: Callable) -> Callable:
    """Decorator for sequentialising all calls to a function.

    To be used with care. The current implementation can't make distinctions,
    so under loads of even just a few RPS things will slow to a crawl.
    """
    queue = asyncio.Queue()

    async def worker() -> None:
        while True:
            coro, future = await queue.get()
            try:
                result = await coro
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                queue.task_done()

    task = None

    @wraps(func)
    async def wrapper(*args, **kwargs):
        nonlocal task
        loop = asyncio.get_event_loop()

        # Start the worker once
        if task is None or task.done():
            task = asyncio.create_task(worker())

        future = loop.create_future()
        await queue.put((func(*args, **kwargs), future))
        return await future

    return wrapper
