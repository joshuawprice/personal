# TODO:
# - Handle the exceptions listed here: https://discordpy.readthedocs.io/en/stable/api.html#discord.Client.connect

import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from .mumble import Mumble

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        await self.add_cog(Mumble(self))

    async def close(self):
        logger.info("Shutting down bot...")
        await super().close()

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
