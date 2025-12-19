import asyncio
import logging
import socket
import struct
import time

from google.protobuf.runtime_version import VersionError

try:
    from . import MumbleUDP_pb2
except VersionError as e:
    e.add_note(
        "Version error on trying to import mumble protobuf python module. "
        "Did you generate it with a newer version than the runtime version?"
    )
    raise e

logger = logging.getLogger(__name__)

# TODO:
# - Mumble SRV record lookup
# - Check return address matches sending address?
# - General tidy:
#   - https://docs.python.org/3/library/asyncio-protocol.html#transports-hierarchy


def encode_ping() -> MumbleUDP_pb2.Ping:
    ping_request = MumbleUDP_pb2.Ping()
    # Mumble "encrypts" this using an XOR so that servers can't spoof the
    # returned timestamp (easily) to fake a better ping
    ping_request.timestamp = int(time.time())
    ping_request.request_extended_information = True

    # The legacy packet format
    # ping_packet = struct.pack(">iQ", 0, int(time.time()))

    # Uses the newer mumble UDP protobuf ping format from MumbleProtocol.cpp
    # "B" is an unsigned char.
    # "c" is a char[], with the length beforehand.
    # 1 is the mumble protobuf UDP ping message type.
    return struct.pack(
        f"B{len(ping_request.SerializeToString())}s",
        1,
        ping_request.SerializeToString(),
    )


# TODO: Timeout socket?
class MumbleClientProtocol:
    def __init__(self, encoded_ping, on_con_lost):
        self.encoded_ping = encoded_ping
        self.on_con_lost = on_con_lost
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        # print("sending")
        self.transport.sendto(self.encoded_ping)

    def datagram_received(self, data, addr):
        # print("receiving")
        _message_type, ping_message_response = struct.unpack(
            f">B{len(data) - 1}s",
            data,
        )

        ping = MumbleUDP_pb2.Ping()
        ping.ParseFromString(ping_message_response)
        self.on_con_lost.set_result(ping.user_count)

        self.transport.close()
        ...

    def error_received(self, exc):
        print("Error received:", exc)

    def connection_lost(self, exc):
        # print("closing")
        if self.on_con_lost.done():
            return

        self.on_con_lost.set_result(None)


async def fetch_user_count(host: str, port: int = 64738) -> int | None:
    loop = asyncio.get_running_loop()

    encoded_ping = encode_ping()
    on_con_lost = loop.create_future()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: MumbleClientProtocol(encoded_ping, on_con_lost),
        remote_addr=(host, port),
    )

    # print("here1")
    try:
        return await on_con_lost
    finally:
        transport.close()


async def _get_server_host():
    loop = asyncio.get_running_loop()

    hosts = ["mumble", "asgard.bifrost"]
    for host in hosts:
        try:
            await loop.getaddrinfo(host, 64738, proto=socket.IPPROTO_UDP)
        except socket.gaierror:
            pass
        else:
            return host
    return "mumble.kruitana.com"


class PingClient:
    def __init__(self):
        self._server_host: str

    async def load(self):
        self._server_host = await _get_server_host()

    async def fetch_user_count(self) -> int | None:
        """Fetch current user count with timeout handling."""
        try:
            async with asyncio.timeout(1):
                logger.debug("Calling fetch_user_count()")
                return await fetch_user_count(self._server_host)
        except TimeoutError:
            # I'm finding a somewhat substantial number of udp pings seem
            # to be getting dropped somewhere, so I guess this is pretty
            # much just normal behaviour.
            logger.debug("Mumble ping timed out")
            return None
