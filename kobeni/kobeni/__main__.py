# TODO:
# - Handle the exceptions listed here: https://discordpy.readthedocs.io/en/stable/api.html#discord.Client.connect

import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from . import mumble


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(__name__)
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        await self.add_cog(mumble.Mumble(self))

    async def close(self):
        self.logger.info("Shutting down bot...")
        await super().close()

    async def on_ready(self):
        self.logger.info(f"We have logged in as {self.user}")


def main():
    load_dotenv()

    intents = discord.Intents.default()
    intents.message_content = True
    bot = Bot(command_prefix="$", intents=intents)

    bot.run(
        os.getenv("TOKEN"),
        # log_level=logging.DEBUG,
        root_logger=True,
    )


if __name__ == "__main__":
    main()
