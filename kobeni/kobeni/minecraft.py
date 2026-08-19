import asyncio
import logging

from discord.ext import commands
from mcstatus import JavaServer

from kobeni import utils
from kobeni.mumble import client
from kobeni.mumble.client import (
    Client,
    ServerEventType,
    UserConnectEvent,
    UserDisconnectEvent,
    UserEvent,
)

logger: logging.Logger = logging.getLogger(__name__)


class MinecraftClient(Client):
    def __init__(self):
        self.user_count: int
        self._server: JavaServer
        self._ping_loop_task: asyncio.Task | None = None

    async def connect(self) -> None:
        if self._ping_loop_task is not None and not self._ping_loop_task.done():
            return

        self._server = await JavaServer.async_lookup("minecraft.qmb.org.uk")
        self.user_count = (await self._server.async_status()).players.online
        self._ping_loop_task = asyncio.create_task(self._ping_loop())

    async def disconnect(self) -> None:
        if self._ping_loop_task is None:
            return

        try:
            del self.user_count
        except AttributeError:
            pass

        self._ping_loop_task.cancel()

    async def _ping(self) -> None:
        last_user_count = self.user_count
        self.user_count = (await self._server.async_status()).players.online

        # Only perform callbacks if there's actually a change on the server.
        if self.user_count is None or self.user_count == last_user_count:
            return

        if self.user_count > last_user_count:
            await self._invoke_callbacks(
                UserConnectEvent(None), last_user_count, self.user_count
            )
        else:
            await self._invoke_callbacks(
                UserDisconnectEvent(None), last_user_count, self.user_count
            )

    async def _ping_loop(self) -> None:
        while True:
            logger.debug("Calling _ping()")
            try:
                await self._ping()
            except Exception:
                pass
            # Was listening to 初恋のこたえ and this happened to be the bpm :)
            await asyncio.sleep(0.3243243243243244)


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

        self.minecraft_client: MinecraftClient = MinecraftClient()

        self.minecraft_client.register_callbacks(self)

        self.voice_channel_id = 1034228938064539661

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Connecting to minecraft server")
        await self.minecraft_client.connect()

        await asyncio.gather(
            self._update_channel_status(
                UserEvent(None), 0, self.minecraft_client.user_count
            )
        )

    async def cog_unload(self):
        logger.info("Unloading minecraft cog...")

        await self.minecraft_client.disconnect()

        general_voice_channel = self.bot.get_channel(self.voice_channel_id)
        await general_voice_channel.edit(status=None)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None:
            return

        # Fix for random status disappearances:
        # When discord.py handles "WebSocket closed with 1006" the bot
        # briefly disconnects, reconnects, then catches up on the events
        # it missed. Because kobeni has already reconnected by the time
        # its disconnect event is replayed, when we check the member
        # list it will contain kobeni, and thus we will incorrectly
        # count the length of the member list as one higher than we
        # should.
        members = [m for m in before.channel.members if m != member]

        # When last user leaves the voice channel, the status disappears.
        if before.channel.id == self.voice_channel_id and len(members) == 0:
            logger.info("Resetting channel status as last discord user has left")
            await self._update_channel_status(
                UserEvent(None), 0, self.minecraft_client.user_count
            )

    @client.on_server_event(ServerEventType.USER_CONNECT)
    @client.on_server_event(ServerEventType.USER_DISCONNECT)
    @utils.sequential
    async def _update_channel_status(
        self,
        event: UserEvent,
        last_user_count: int,
        user_count: int,
    ) -> None:
        """Update Discord channel status with current user count."""
        channel = self.bot.get_channel(self.voice_channel_id)
        pluralised_user_string = "player" if user_count == 1 else "players"

        status = f"{user_count} {pluralised_user_string} on Minecraft"
        logger.info(
            f"Setting status of {channel.name} in {channel.guild.name} to: {status}"
        )
        await channel.edit(status=status)

    @client.on_server_event(ServerEventType.USER_CONNECT)
    @client.on_server_event(ServerEventType.USER_DISCONNECT)
    @utils.sequential
    async def _manage_voice_connection(
        self,
        event: UserEvent,
        last_user_count: int,
        user_count: int,
    ) -> None:
        """Connect or disconnect voice client based on user count."""
        channel = self.bot.get_channel(self.voice_channel_id)
        guild = channel.guild
        voice_client = guild.voice_client

        if user_count > 0 and voice_client is None:
            logger.info(f"Connecting to {channel.name} in {guild.name}")
            await channel.connect(self_mute=True, self_deaf=True)
        elif user_count == 0 and voice_client is not None:
            logger.info(f"Disconnecting from {channel.name} in {guild.name}")
            await voice_client.disconnect()
