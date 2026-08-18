import asyncio
import time
from unittest.mock import AsyncMock, patch

import pytest

from kobeni.minecraft import MinecraftClient


async def test_ping_loop_pings_and_sleeps_correctly():
    minecraft_client = MinecraftClient()
    ping = AsyncMock()
    minecraft_client._ping = ping

    calls = 0

    async def sleep(interval: float) -> None:
        nonlocal calls
        calls += 1

        if calls >= 3:
            raise asyncio.CancelledError()

    with (
        pytest.raises(asyncio.CancelledError),
        patch("kobeni.minecraft.asyncio.sleep", new=sleep),
    ):
        await asyncio.wait_for(minecraft_client._ping_loop(), timeout=1)

    assert ping.await_count == 3


async def test_ping_loop_continues_after_ping_failure():
    minecraft_client = MinecraftClient()
    ping = AsyncMock(
        side_effect=[
            RuntimeError("loop did not gracefully continue after ping failed.")
        ]
    )
    minecraft_client._ping = ping

    async def sleep(_):
        raise asyncio.CancelledError()

    with (
        pytest.raises(asyncio.CancelledError),
        patch("kobeni.minecraft.asyncio.sleep", new=sleep),
    ):
        await asyncio.wait_for(minecraft_client._ping_loop(), timeout=1)

    assert ping.await_count == 1
