# TODO:
# - Handle the exceptions listed here: https://discordpy.readthedocs.io/en/stable/api.html#discord.Client.connect

import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from . import mumble


class Bot(commands.Bot):
    async def setup_hook(self):
        await bot.add_cog(mumble.Mumble(bot))

    async def close(self):
        logger.info("Shutting down bot...")
        await super().close()

    async def on_ready(self):
        logger.info(f"We have logged in as {self.user}")


def main(): ...


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    load_dotenv()

    intents = discord.Intents.default()
    intents.message_content = True
    bot = Bot(command_prefix="$", intents=intents)

    bot.run(
        os.getenv("TOKEN"),
        # log_level=logging.DEBUG,
        root_logger=True,
    )

    main()
