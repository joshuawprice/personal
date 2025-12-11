import asyncio
from datetime import datetime, timedelta, timezone
import json
import logging
from pathlib import Path
import socket
import struct
import time
import os

import discord
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


class NotifyUsers:
    """
    Manages the list of users to receive notifications when the mumble server becomes active.
    """

    def __init__(self, bot):
        logger = logging.getLogger(__name__)

        config: Path = Path("config")
        config.mkdir(exist_ok=True)
        self._backing_file: Path = config / "mumble-notify-users.json"

        self._users: list[discord.User] = []
        try:
            with open(self._backing_file) as f:
                user_ids: list[int] = json.load(f)
                self._users = [bot.get_user(id) for id in user_ids]
        except FileNotFoundError:
            self._users = []
            logger.debug(f"{self._backing_file} not found. Starting from scratch.")
            pass
        except (json.JSONDecodeError, UnicodeDecodeError):
            logger.warning(
                "Error reading list of users to be notified. Starting from scratch."
            )

    def __contains__(self, user: discord.User, /):
        return self._users.__contains__(user)

    def __getitem__(self, key):
        return self._users.__getitem__(key)

    def __len__(self):
        return self._users.__len__()

    def append(self, user, /):
        self._users.append(user)

        with open(self._backing_file, "w") as f:
            json.dump([user.id for user in self._users], f)

    def remove(self, user, /):
        self._users.remove(user)

        with open(self._backing_file, "w") as f:
            json.dump([user.id for user in self._users], f)


class Mumble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.server_host = None
        self.last_user_count = None
        self.users = None
        self.last_iteration = datetime.now(timezone.utc) - timedelta(minutes=1.67)

        voice_channel_id = os.getenv("MUMBLE_CHANNEL")
        if voice_channel_id is None:
            raise ValueError("Missing MUMBLE_CHANNEL env var.")
        self.voice_channel_id = int(voice_channel_id)

    async def cog_load(self):
        self.server_host = await _get_server_host()
        self.logger.info("Setting mumble server_host to: " + self.server_host)

        self.ping_loop.start()

    async def cog_unload(self):
        self.logger.info("Unloading mumble cog...")

        self.ping_loop.cancel()
        general_voice_channel = self.bot.get_channel(self.voice_channel_id)
        await general_voice_channel.edit(status=None)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None:
            return

        # When last user leaves the voice channel, the status disappears.
        if (
            before.channel.id == self.voice_channel_id
            and len(before.channel.members) == 0
        ):
            # Required to force the channel status to update
            self.last_user_count = None

            await self.ping_loop()

    @commands.command()
    async def notify(self, ctx):
        """
        Toggles DM notifications for activity on the Mumble server
        """
        user = ctx.message.author

        if user in self.users:
            self.users.remove(user)
            await ctx.message.add_reaction("🔕")
        else:
            self.users.append(user)
            await ctx.message.add_reaction("🔔")

    def _is_ping_loop_behind(self) -> bool:
        """Check if loop has fallen behind and needs restart."""
        current_time = datetime.now(timezone.utc)
        next_iteration_time = self.ping_loop.next_iteration
        return next_iteration_time is not None and current_time >= next_iteration_time

    async def _fetch_current_user_count(self) -> int | None:
        """Fetch current user count with timeout handling."""
        try:
            async with asyncio.timeout(1):
                self.logger.debug(f'Calling fetch_user_count("{self.server_host}")')
                return await fetch_user_count(self.server_host)
        except TimeoutError:
            # I'm finding a somewhat substantial number of udp pings seem
            # to be getting dropped somewhere, so I guess this is pretty
            # much just normal behaviour.
            self.logger.debug("Mumble ping timed out")
            return None

    async def _update_channel_status(self, user_count: int) -> None:
        """Update Discord channel status with current user count."""
        channel = self.bot.get_channel(self.voice_channel_id)
        pluralised_user_string = "user" if user_count == 1 else "users"

        self.logger.info(f"Updating status of {channel.name} in {channel.guild.name}")
        await channel.edit(status=f"{user_count} {pluralised_user_string} on Mumble")

    async def _manage_voice_connection(self, user_count: int) -> None:
        """Connect or disconnect voice client based on user count."""
        channel = self.bot.get_channel(self.voice_channel_id)
        guild = channel.guild
        voice_client = guild.voice_client

        if user_count > 0 and voice_client is None:
            self.logger.info(f"Connecting to {channel.name} in {guild.name}")
            await channel.connect(self_mute=True, self_deaf=True)
        elif user_count == 0 and voice_client is not None:
            self.logger.info(f"Disconnecting from {channel.name} in {guild.name}")
            await voice_client.disconnect()

    async def _send_notifications_if_needed(self, user_count: int) -> None:
        """Send notifications when Mumble becomes active after cooldown."""
        if not (self.last_user_count == 0 and user_count > 0):
            return

        if self._is_on_cooldown():
            self.logger.info("Not pinging due to cooldown.")
            return

        self.logger.info("Pinging users for Mumble")
        msg = "Mumble just became active!"
        results = await asyncio.gather(
            *[self._send_notification(user, msg) for user in self.users],
            return_exceptions=True,
        )

        for user, result in zip(self.users, results):
            if isinstance(result, Exception):
                self.logger.warning(f"Failed to notify {user}: {result}")

    def _is_on_cooldown(self) -> bool:
        """Check if notification cooldown is active."""
        cooldown_period = timedelta(minutes=2)
        time_since_last = datetime.now(timezone.utc) - self.last_iteration
        return time_since_last <= cooldown_period

    async def _send_notification(self, user, msg):
        """Helper method to send DM notification."""
        dm = user.dm_channel or await user.create_dm()
        await dm.send(msg)

    # Was listening to 初恋のこたえ and this happened to be the bpm :)
    @tasks.loop(seconds=0.3243243243243244)
    async def ping_loop(self):
        self.logger.debug("Entering ping_loop()")

        # If the loop gets behind, it will try to catchup all delayed runs.
        # This just prevents it doing that and spamming the server.
        if self._is_ping_loop_behind():
            self.logger.debug("Restarting ping_loop() task")
            self.ping_loop.restart()
            return

        current_user_count = await self._fetch_current_user_count()

        # Only update discord if there's actually a change on the server.
        if current_user_count is None or current_user_count == self.last_user_count:
            return

        await asyncio.gather(
            self._update_channel_status(current_user_count),
            self._manage_voice_connection(current_user_count),
            self._send_notifications_if_needed(current_user_count),
        )

        self.last_user_count = current_user_count
        self.last_iteration = datetime.now(timezone.utc)

    # This runs even on loop.restart()
    @ping_loop.before_loop
    async def wait_until_ready(self):
        await self.bot.wait_until_ready()
        # Must wait until the member cache is populated.
        self.users = NotifyUsers(self.bot)
