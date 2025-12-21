import asyncio
from datetime import datetime, timedelta, timezone
import json
import logging
from pathlib import Path
import os

import discord
from discord.ext import commands

from .ping_client import PingClient

logger: logging.Logger = logging.getLogger(__name__)


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
        self.bot: commands.Bot = bot

        self.mumble_client: PingClient = PingClient()

        for name in dir(self):
            method = getattr(self, name)
            if callable(method) and getattr(
                method, "_mumble_client_on_user_presence_changed", False
            ):
                self.mumble_client.add_user_presence_changed_callback(method)

        self.users = None
        self.notifications_last_sent_at: datetime = datetime.min.replace(
            tzinfo=timezone.utc
        )

        voice_channel_id = os.getenv("MUMBLE_CHANNEL")
        if voice_channel_id is None:
            raise ValueError("Missing MUMBLE_CHANNEL env var.")
        self.voice_channel_id = int(voice_channel_id)

    @commands.Cog.listener()
    async def on_ready(self):
        self.users = NotifyUsers(self.bot)

        logger.info("Calling mumble_client.connect()")
        await self.mumble_client.connect()

        await asyncio.gather(
            self._update_channel_status(0, self.mumble_client.user_count),
            self._manage_voice_connection(0, self.mumble_client.user_count),
        )

    async def cog_unload(self):
        logger.info("Unloading mumble cog...")

        await self.mumble_client.disconnect()

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
            await self._update_channel_status(0, self.mumble_client.user_count)

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

    def on_mumble_user_presence_changed(f):
        f._mumble_client_on_user_presence_changed = True
        return f

    @on_mumble_user_presence_changed
    async def _update_channel_status(
        self, last_user_count: int, user_count: int
    ) -> None:
        """Update Discord channel status with current user count."""
        channel = self.bot.get_channel(self.voice_channel_id)
        pluralised_user_string = "user" if user_count == 1 else "users"

        logger.info(f"Updating status of {channel.name} in {channel.guild.name}")
        await channel.edit(status=f"{user_count} {pluralised_user_string} on Mumble")

    @on_mumble_user_presence_changed
    async def _manage_voice_connection(
        self, last_user_count: int, user_count: int
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

    @on_mumble_user_presence_changed
    async def _send_notifications_if_needed(
        self, last_user_count: int, user_count: int
    ) -> None:
        """Send notifications when Mumble becomes active after cooldown."""
        if not (last_user_count == 0 and user_count > 0):
            self.notifications_last_sent_at = datetime.now(timezone.utc)
            return

        if self._is_on_cooldown():
            logger.info("Not pinging due to cooldown.")
            return

        logger.info("Pinging users for Mumble")
        msg = "Mumble just became active!"
        results = await asyncio.gather(
            *[self._send_notification(user, msg) for user in self.users],
            return_exceptions=True,
        )

        for user, result in zip(self.users, results):
            if isinstance(result, Exception):
                logger.warning(f"Failed to notify {user}: {result}")

        self.notifications_last_sent_at = datetime.now(timezone.utc)

    def _is_on_cooldown(self) -> bool:
        """Check if notification cooldown is active."""
        cooldown_period = timedelta(minutes=2)
        time_since_last = datetime.now(timezone.utc) - self.notifications_last_sent_at
        return time_since_last <= cooldown_period

    async def _send_notification(self, user, msg):
        """Helper method to send DM notification."""
        dm = user.dm_channel or await user.create_dm()
        await dm.send(msg)
