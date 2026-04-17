# TODO:
# - Handle the exceptions listed here: https://discordpy.readthedocs.io/en/stable/api.html#discord.Client.connect

import asyncio
import functools
import logging
import os
import signal

import discord
from discord.ext import commands
from dotenv import load_dotenv

from .mumble import Mumble

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle_shutdown_event(self, signal: str):
        logger.info(f"{signal} received, shutting down...")
        asyncio.create_task(self.close())

    async def setup_hook(self):
        # Setup signals to shutdown properly. discord.py only handles SIGINT by default.
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(
            signal.SIGINT, functools.partial(self.handle_shutdown_event, "SIGINT")
        )
        loop.add_signal_handler(
            signal.SIGTERM, functools.partial(self.handle_shutdown_event, "SIGTERM")
        )

        await self.add_cog(Mumble(self))

    async def on_ready(self):
        logger.info(f"We have logged in as {self.user}")


def main():
    load_dotenv()
    discord.utils.setup_logging()

    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    prefix = os.getenv("PREFIX") or "!"
    logger.info(f"Setting prefix: {prefix}")

    bot = Bot(command_prefix=prefix, intents=intents)

    if not os.getenv("TOKEN"):
        raise ValueError("Missing discord token.")

    bot.run(os.getenv("TOKEN"), log_handler=None)
