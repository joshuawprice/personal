from collections.abc import Awaitable, Callable


def on_user_connect(f):
    f._on_mumble_client_user_connect = True
    return f


def on_user_disconnect(f):
    f._on_mumble_client_user_disconnect = True
    return f


class Client:
    async def connect(self) -> None:
        raise NotImplementedError

    async def disconnect(self) -> None:
        raise NotImplementedError

    def register_callbacks(self, obj):
        for name in dir(obj):
            method = getattr(obj, name)
            if not callable(method):
                continue

            if getattr(method, "_on_mumble_client_user_connect", False):
                self.add_user_connect_callback(method)
            if getattr(method, "_on_mumble_client_user_disconnect", False):
                self.add_user_disconnect_callback(method)

    def add_user_presence_changed_callback(
        self, func: Callable[[int, int], Awaitable]
    ) -> None:
        raise NotImplementedError
