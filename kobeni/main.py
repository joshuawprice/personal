# TODO:
# - Handle the exceptions listed here: https://discordpy.readthedocs.io/en/stable/api.html#discord.Client.connect
# - Don't expose the token!!
# - Switch to using discord.ext cogs and whatnot

import asyncio
from datetime import datetime, timezone
import logging

import discord
from discord.ext import tasks

import mumble


GENERAL_VOICE_CHANNEL_ID = 532274742141517828

last_user_count = None


class MyClient(discord.Client):
    async def setup_hook(self):
        update_mumble_user_count.start()

    async def close(self):
        logger.info("Shutting down bot...")
        update_mumble_user_count.cancel()
        await remove_mumble_channel_count_status()
        await super().close()

    async def on_ready(self):
        logger.info(f"We have logged in as {self.user}")

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith("$hello"):
            await message.channel.send("Hello!")

    async def on_voice_state_update(self, member, before, after):
        if before.channel is None:
            return

        # When last user leaves the voice channel, the status disappears.
        if (
            before.channel.id == GENERAL_VOICE_CHANNEL_ID
            and len(before.channel.members) == 0
        ):
            # Required to force the channel status to update
            global last_user_count
            last_user_count = None

            await update_mumble_user_count()


# Was listening to 初恋のこたえ and this happened to be the bpm :)
@tasks.loop(seconds=0.3243243243243244)
async def update_mumble_user_count():
    logger.debug("Entering update_mumble_user_count()")

    # If the loop gets behind, it will try to catchup all delayed runs.
    # This just prevents it doing that and spamming the server.
    current_time = datetime.now(timezone.utc)
    next_iteration_time = update_mumble_user_count.next_iteration
    if current_time >= next_iteration_time:
        logger.debug("Restarting update_mumble_user_count() task")
        update_mumble_user_count.restart()

    try:
        async with asyncio.timeout(1):
            logger.debug("Calling mumble.fetch_user_count()")
            current_user_count = await mumble.fetch_user_count("asgard.bifrost")
    except TimeoutError:
        # I'm finding a somewhat substantial number of udp pings seem
        # to be getting dropped somewhere, so I guess this is pretty
        # much just normal behaviour.
        logger.debug("Mumble ping timed out")
        return

    global last_user_count
    if current_user_count == last_user_count:
        return

    last_user_count = current_user_count

    general_voice_channel = client.get_channel(GENERAL_VOICE_CHANNEL_ID)
    pluralised_user_string = "users" if current_user_count != 1 else "user"
    logger.debug("Updating status of general voice channel in jp")
    await general_voice_channel.edit(
        status=f"{current_user_count} {pluralised_user_string} on Mumble"
    )

    voice_client = client.get_guild(532274742141517824).voice_client
    if current_user_count > 0 and voice_client is None:
        logger.debug("Connecting to general voice channel in jp")
        await general_voice_channel.connect()
    elif current_user_count == 0 and voice_client is not None:
        logger.debug("Disconnecting from general voice channel in jp")
        await voice_client.disconnect()


@update_mumble_user_count.before_loop
async def wait_until_ready():
    await client.wait_until_ready()


async def remove_mumble_channel_count_status():
    general_voice_channel = client.get_channel(GENERAL_VOICE_CHANNEL_ID)
    await general_voice_channel.edit(status=None)


def main(): ...


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)

    client.run(
        "",
        log_level=logging.DEBUG,
        root_logger=True,
    )

    main()
