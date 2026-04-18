from abc import ABC, abstractmethod
import asyncio
from collections.abc import Awaitable, Callable
from enum import auto, Enum
from functools import wraps
import logging
import traceback

logger = logging.getLogger(__name__)


class ServerEvent(Enum):
    """All server events that run callbacks."""

    USER_CONNECT = auto()
    USER_DISCONNECT = auto()
    USER_CHANGE = auto()
    USER_TEXT_MESSAGE = auto()
    CHANNEL_CREATE = auto()
    CHANNEL_DELETE = auto()
    CHANNEL_CHANGE = auto()


def on_user_connect(f):
    f._on_mumble_client_user_connect = True
    return f


def on_user_disconnect(f):
    f._on_mumble_client_user_disconnect = True
    return f


class Client(ABC):
    def __init__(self):
        self._callbacks: dict[str, set[Callable[[int, int], Awaitable]]] = {
            ServerEvent.USER_CONNECT: set(),
            ServerEvent.USER_DISCONNECT: set(),
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
                self._callbacks[ServerEvent.USER_CONNECT].add(method)
            if getattr(method, "_on_mumble_client_user_disconnect", False):
                self._callbacks[ServerEvent.USER_DISCONNECT].add(method)

    async def invoke_user_connect_callbacks(self, last_user_count, user_count) -> None:
        results = await asyncio.gather(
            *(
                f(last_user_count, user_count)
                for f in self._callbacks[ServerEvent.USER_CONNECT]
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
                for f in self._callbacks[ServerEvent.USER_DISCONNECT]
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
