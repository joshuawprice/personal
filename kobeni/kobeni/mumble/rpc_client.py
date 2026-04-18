import asyncio
import logging
import os
import sys

import Ice

# The MumbleServer module uses absolute imports for sibling modules.
sys.path.insert(0, os.path.dirname(__file__))
import MumbleServer

from .client import (
    Client,
    ServerEventType,
    User,
    ServerEvent,
    UserConnectEvent,
    UserDisconnectEvent,
)

logger = logging.getLogger(__name__)


def user_from_ice(ice_user: MumbleServer.User) -> User:
    return User(name=ice_user.name)


class ServerCallback(MumbleServer.ServerCallback):
    def __init__(self, rpc_client):
        self.rpc_client = rpc_client

    async def userConnected(self, user: MumbleServer.User, current):
        await self.rpc_client.on_ice_callback(UserConnectEvent(user_from_ice(user)))

    async def userDisconnected(self, user: MumbleServer.User, current):
        await self.rpc_client.on_ice_callback(UserDisconnectEvent(user_from_ice(user)))

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

        self.user_count: int = 0

        # For reconciling state between setting up callbacks and getting initial state.
        self._buffer: list
        self._live: bool = False

    async def connect(self):
        self.ice_communicator = Ice.Communicator(eventLoop=asyncio.get_event_loop())

        # TODO: Get host dynamically
        meta = MumbleServer.MetaPrx(
            self.ice_communicator, "Meta:tcp -h mumble -p 6502 -t 60000"
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

        await self.server.addCallbackAsync(callback_proxy)
        self.user_count = len(await self.server.getUsersAsync())

        for event in self._buffer:
            self.on_ice_callback(event)

        self._live = True

    async def disconnect(self):
        self._live = False
        # Remove callbacks?

        await self.ice_communicator.destroyAsync()
        self.ice_communicator = None

    async def on_ice_callback(self, event: ServerEvent):
        if not self._live:
            self._buffer.append(event)
            return

        last_user_count = self.user_count

        match event.type:
            case ServerEventType.USER_CONNECT:
                self.user_count += 1
            case ServerEventType.USER_DISCONNECT:
                self.user_count -= 1

        await self._invoke_callbacks(event.type, last_user_count, self.user_count)
