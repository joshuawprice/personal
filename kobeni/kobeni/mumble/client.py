from collections.abc import Awaitable, Callable


class Client:
    async def connect(self) -> None:
        raise NotImplementedError

    async def disconnect(self) -> None:
        raise NotImplementedError

    def add_user_presence_changed_callback(
        self, func: Callable[[int, int], Awaitable]
    ) -> None:
        raise NotImplementedError
