import asyncio
from datetime import datetime, timezone
import logging
import struct
import time

from discord.ext import commands, tasks
from google.protobuf.runtime_version import VersionError

try:
    from . import MumbleUDP_pb2
except VersionError as e:
    print(
        "Version error on trying to import mumble protobuf python module. "
        "Did you generate it with a newer version than the runtime version?"
    )
    raise e

# TODO:
# - Mumble SRV record lookup
# - Check return address matches sending address?
# - General tidy:
#   - https://docs.python.org/3/library/asyncio-protocol.html#transports-hierarchy
# - Pick a better way of getting the address to ping (eg asgard.bifrost/jprice.uk)


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


async def fetch_user_count(host, port=64738) -> int | None:
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


class Mumble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.last_user_count = None
        self.GENERAL_VOICE_CHANNEL_ID = 532274742141517828

    async def cog_load(self):
        self.update_mumble_user_count.start()

    async def cog_unload(self):
        self.logger.info("Unloading mumble cog...")

        self.update_mumble_user_count.cancel()
        general_voice_channel = self.bot.get_channel(self.GENERAL_VOICE_CHANNEL_ID)
        await general_voice_channel.edit(status=None)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None:
            return

        # When last user leaves the voice channel, the status disappears.
        if (
            before.channel.id == self.GENERAL_VOICE_CHANNEL_ID
            and len(before.channel.members) == 0
        ):
            # Required to force the channel status to update
            self.last_user_count = None

            await self.update_mumble_user_count()

    # Was listening to 初恋のこたえ and this happened to be the bpm :)
    @tasks.loop(seconds=0.3243243243243244)
    async def update_mumble_user_count(self):
        self.logger.debug("Entering update_mumble_user_count()")

        # If the loop gets behind, it will try to catchup all delayed runs.
        # This just prevents it doing that and spamming the server.
        current_time = datetime.now(timezone.utc)
        next_iteration_time = self.update_mumble_user_count.next_iteration
        if next_iteration_time is not None and current_time >= next_iteration_time:
            self.logger.debug("Restarting update_mumble_user_count() task")
            self.update_mumble_user_count.restart()
            return

        try:
            async with asyncio.timeout(1):
                self.logger.debug("Calling mumble.fetch_user_count()")
                current_user_count = await fetch_user_count("asgard.bifrost")
        except TimeoutError:
            # I'm finding a somewhat substantial number of udp pings seem
            # to be getting dropped somewhere, so I guess this is pretty
            # much just normal behaviour.
            self.logger.debug("Mumble ping timed out")
            return

        if current_user_count == self.last_user_count:
            return

        self.last_user_count = current_user_count

        general_voice_channel = self.bot.get_channel(self.GENERAL_VOICE_CHANNEL_ID)
        pluralised_user_string = "users" if current_user_count != 1 else "user"
        self.logger.info("Updating status of general voice channel in jp")
        await general_voice_channel.edit(
            status=f"{current_user_count} {pluralised_user_string} on Mumble"
        )

        voice_client = self.bot.get_guild(532274742141517824).voice_client
        if current_user_count > 0 and voice_client is None:
            self.logger.info("Connecting to general voice channel in jp")
            await general_voice_channel.connect()
        elif current_user_count == 0 and voice_client is not None:
            self.logger.info("Disconnecting from general voice channel in jp")
            await voice_client.disconnect()

    @update_mumble_user_count.before_loop
    async def wait_until_ready(self):
        await self.bot.wait_until_ready()
