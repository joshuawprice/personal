import asyncio
from functools import wraps
import logging

from discord.ext import commands
from mcstatus import JavaServer

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
            await self._ping()
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

    # To be used with care. The current implementation can't make
    # distinctions, so under loads of even just a few RPS things will
    # slow to a crawl.
    def sequential(func: Callable) -> Callable:
        queue = asyncio.Queue()

        async def worker() -> None:
            while True:
                coro, future = await queue.get()
                try:
                    result = await coro
                    future.set_result(result)
                except Exception as e:
                    future.set_exception(e)
                finally:
                    queue.task_done()

        task = None

        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal task
            loop = asyncio.get_event_loop()

            # Start the worker once
            if task is None or task.done():
                task = asyncio.create_task(worker())

            future = loop.create_future()
            await queue.put((func(*args, **kwargs), future))
            return await future

        return wrapper

    @client.on_server_event(ServerEventType.USER_CONNECT)
    @client.on_server_event(ServerEventType.USER_DISCONNECT)
    @sequential
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
