from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from functools import wraps


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
