import asyncio
from collections.abc import Awaitable, Callable
import logging
import traceback

import Ice
from . import MumbleServer

from .client import Client

logger = logging.getLogger(__name__)


class ServerCallback(MumbleServer.ServerCallback):
    def __init__(self, rpc_client):
        self.rpc_client = rpc_client

    async def userConnected(self, user, current):
        await self.rpc_client.on_user_connect(user)

    async def userDisconnected(self, user, current):
        await self.rpc_client.on_user_disconnect(user)

    async def channelCreated(self, state, current):
        pass

    async def channelRemoved(self, state, current):
        pass

    async def channelStateChanged(self, state, current):
        pass

    async def userStateChanged(self, state, current):
        pass

    async def userTextMessage(self, state, message, current):
        pass


class RpcClient(Client):
    def __init__(self):
        self.ice_communicator: Ice.Communicator | None
        self.server: MumbleServer.ServerPrx
        self._callbacks: dict[str, set[Callable[[int, int], Awaitable]]] = {
            "on_user_connect": set(),
            "on_user_disconnect": set(),
        }
        self.user_count: int = 0

        # For reconciling state between setting up callbacks and getting initial state.
        self._buffer: list
        self._live: bool

    async def connect(self):
        self.ice_communicator = Ice.Communicator(eventLoop=asyncio.get_event_loop())

        # TODO: Get host dynamically
        meta = MumbleServer.MetaPrx(
            self.ice_communicator, "Meta:tcp -h mumble-server -p 6502 -t 60000"
        )

        # This should only be the one server retrieved for now.
        self.server = (await meta.getAllServersAsync())[0]

        # For some reason the proxy uses the internal docker ip address, which
        # of course is not accessible from my local machine.
        #
        # A little gross, but I couldn't get Ice.Default.Host property to work.
        # TODO: This may not be necessary when the discord bot and mumble server
        #       are running on the same host.
        endpoint = meta.ice_getEndpoints()
        self.server = self.server.ice_endpoints((endpoint))

        # Add callbacks
        adapter = self.ice_communicator.createObjectAdapterWithEndpoints(
            "ServerCallbackAdapter", "tcp"
        )
        callback_proxy = adapter.add(
            ServerCallback(self), Ice.Identity(name="server_callback")
        )
        adapter.activate()

        self._buffer = []
        self._live = False

        await self.server.addCallbackAsync(callback_proxy)
        users = await self.server.getUsersAsync()

        for event in self._buffer:
            if event["type"] == "connect":
                users[event["user"].session] = event["user"]
            elif event["type"] == "disconnect":
                users.pop(event["user"].session, None)

        self.user_count = len(users)
        self._live = True

    async def disconnect(self):
        # Remove callbacks?

        await self.ice_communicator.destroyAsync()
        self.ice_communicator = None

    def add_user_connect_callback(self, func: Callable[[int, int], Awaitable]) -> None:
        self._callbacks["on_user_connect"].add(func)

    def add_user_disconnect_callback(
        self, func: Callable[[int, int], Awaitable]
    ) -> None:
        self._callbacks["on_user_disconnect"].add(func)

    async def on_user_connect(self, user: MumbleServer.User):
        if not self._live:
            self._buffer.append({"type": "connect", "user": user})
            return

        last_user_count = self.user_count
        self.user_count += 1

        results = await asyncio.gather(
            *(
                f(last_user_count, self.user_count)
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

    async def on_user_disconnect(self, user: MumbleServer.User):
        if not self._live:
            self._buffer.append({"type": "disconnect", "user": user})
            return

        last_user_count = self.user_count
        self.user_count -= 1

        results = await asyncio.gather(
            *(
                f(last_user_count, self.user_count)
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
