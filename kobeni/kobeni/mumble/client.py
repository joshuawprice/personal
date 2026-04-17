from abc import ABC, abstractmethod
import asyncio
from collections.abc import Awaitable, Callable
from functools import wraps
import logging
import traceback

logger = logging.getLogger(__name__)


def on_user_connect(f):
    f._on_mumble_client_user_connect = True
    return f


def on_user_disconnect(f):
    f._on_mumble_client_user_disconnect = True
    return f


class Client(ABC):
    def __init__(self):
        self._callbacks: dict[str, set[Callable[[int, int], Awaitable]]] = {
            "on_user_connect": set(),
            "on_user_disconnect": set(),
        }

    def __init_subclass__(cls, **kwargs):
        """Automatically calls Client's init when subclass is instantiated."""
        super().__init_subclass__(**kwargs)
        if "__init__" not in cls.__dict__:
            return
        original_init = cls.__init__

        @wraps(original_init)
        def new_init(self, *args, **kw):
            original_init(self, *args, **kw)
            super(cls, self).__init__()

        cls.__init__ = new_init

    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    def register_callbacks(self, obj):
        for name in dir(obj):
            method = getattr(obj, name)
            if not callable(method):
                continue

            if getattr(method, "_on_mumble_client_user_connect", False):
                self.add_user_connect_callback(method)
            if getattr(method, "_on_mumble_client_user_disconnect", False):
                self.add_user_disconnect_callback(method)

    def add_user_connect_callback(self, func: Callable[[int, int], Awaitable]) -> None:
        self._callbacks["on_user_connect"].add(func)

    def add_user_disconnect_callback(
        self, func: Callable[[int, int], Awaitable]
    ) -> None:
        self._callbacks["on_user_disconnect"].add(func)

    async def invoke_user_connect_callbacks(self, last_user_count, user_count) -> None:
        results = await asyncio.gather(
            *(
                f(last_user_count, user_count)
                for f in self._callbacks["on_user_connect"]
            ),
            return_exceptions=True,
        )

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                tb_str = "".join(
                    traceback.format_exception(
                        type(result), result, result.__traceback__
                    )
                )
                logger.warning(f"Task {i} failed:\n{tb_str}")

    async def invoke_user_disconnect_callbacks(
        self, last_user_count, user_count
    ) -> None:
        results = await asyncio.gather(
            *(
                f(last_user_count, user_count)
                for f in self._callbacks["on_user_disconnect"]
            ),
            return_exceptions=True,
        )

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                tb_str = "".join(
                    traceback.format_exception(
                        type(result), result, result.__traceback__
                    )
                )
                logger.warning(f"Task {i} failed:\n{tb_str}")
