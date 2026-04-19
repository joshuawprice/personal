from abc import ABC, abstractmethod
import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from enum import auto, Enum
from functools import wraps
import logging
import traceback
from typing import ClassVar

logger = logging.getLogger(__name__)


class ServerEventType(Enum):
    """All server events that run callbacks."""

    USER_CONNECT = auto()
    USER_DISCONNECT = auto()
    USER_CHANGE = auto()
    USER_TEXT_MESSAGE = auto()
    CHANNEL_CREATE = auto()
    CHANNEL_DELETE = auto()
    CHANNEL_CHANGE = auto()


@dataclass(frozen=True)
class User:
    name: str


@dataclass(frozen=True)
class ServerEvent:
    type: ClassVar[ServerEventType]


@dataclass(frozen=True)
class UserEvent(ServerEvent):
    user: User | None


@dataclass(frozen=True)
class UserConnectEvent(UserEvent):
    type = ServerEventType.USER_CONNECT


@dataclass(frozen=True)
class UserDisconnectEvent(UserEvent):
    type = ServerEventType.USER_DISCONNECT


def on_server_event(*events: ServerEventType) -> Callable:
    def decorator(f: Callable) -> Callable:
        registered_events: set = getattr(f, "_on_mumble_event", set())
        f._on_mumble_event = registered_events.union(events)
        return f

    return decorator


class Client(ABC):
    def __init__(self):
        self._callbacks: dict[str, set[Callable[[int, int], Awaitable]]] = {
            ServerEventType.USER_CONNECT: set(),
            ServerEventType.USER_DISCONNECT: set(),
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

            events = getattr(method, "_on_mumble_event", None)
            if not events:
                continue

            for event in events:
                self._callbacks[event].add(method)

    async def _invoke_callbacks(
        self, event: ServerEvent, last_user_count: int, user_count: int
    ) -> None:
        results = await asyncio.gather(
            *(
                f(event, last_user_count, user_count)
                for f in self._callbacks[event.type]
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
