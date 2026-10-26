import asyncio
import logging
import os
from datetime import UTC, datetime, timedelta
from urllib.parse import quote

import httpx

API = "https://api.myday.cloud"
TOKEN_URL = f"{API}/sessions/token"
CALENDAR_URL = f"{API}/legacy/api/aggregate/v2/calendaritem"
CLIENT_ID = "myday-web-4e0f11f9-046e-4505-9cb8-db2152311e21"

EXTEND_EVERY_N_RENEWALS = 4
TOKEN_MARGIN_SECS = 60
MAX_BACKOFF_SECS = 300

log = logging.getLogger("myday")


class MydaySession:
    def __init__(
        self,
        client: httpx.AsyncClient,
        *,
        session_id: str,
        id_token: str,
        device_code: str,
    ):
        self.client = client
        self.session_id = session_id
        self.id_token = id_token
        self.device_code = device_code
        self.access_token: str | None = None
        self._ready = asyncio.Event()
        self._task: asyncio.Task | None = None

    @property
    def _extend_url(self) -> str:
        return f"{API}/sessions/session/{self.session_id}/extend"

    async def __aenter__(self):
        self._task = asyncio.create_task(self._loop())
        await self._ready.wait()  # first token available
        return self

    async def __aexit__(self, *exc):
        if self._task:
            self._task.cancel()
            await asyncio.gather(self._task, return_exceptions=True)

    async def renew(self) -> int:
        """Fetch a new access token; return its lifetime in seconds."""
        r = await self.client.post(
            TOKEN_URL,
            data={
                "grant_type": "get_token",
                "client_id": CLIENT_ID,
                "id_token": self.id_token,
                "code": self.device_code,
            },
        )
        r.raise_for_status()
        d = r.json()
        self.access_token = d["access_token"]
        self._ready.set()
        log.info("token renewed, expires_in=%s", d["expires_in"])
        return int(d["expires_in"])

    async def session_extend(self) -> None:
        r = await self.client.post(
            self._extend_url,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        r.raise_for_status()
        d = r.json()
        log.info(
            "session extended, expires=%s (in %ss)",
            d["sessionExpires"],
            d["sessionExpiresInSecs"],
        )

    async def _loop(self):
        renewals, backoff = 0, 5
        while True:
            try:
                expires_in = await self.renew()
                renewals += 1
                if renewals % EXTEND_EVERY_N_RENEWALS == 0:
                    await self.session_extend()
                backoff = 5
                delay = max(expires_in - TOKEN_MARGIN_SECS, 30)
            except httpx.HTTPError as e:
                log.warning("request failed: %r; retry in %ss", e, backoff)
                delay = backoff
                backoff = min(backoff * 2, MAX_BACKOFF_SECS)
            await asyncio.sleep(delay)

    async def get_calendar(self, past_days: int = 28, future_days: int = 28 * 2) -> dict:
        now = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
        fmt = "%Y-%m-%dT%H:%M:%SZ"
        start = (now - timedelta(days=past_days)).strftime(fmt)
        end = (now + timedelta(days=future_days)).strftime(fmt)
        flt = f"End gt datetime'{start}' and Start lt datetime'{end}'"
        r = await self.client.get(
            f"{CALENDAR_URL}?$filter={quote(flt, safe="'")}",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        r.raise_for_status()
        return r.json()


async def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    async with (
        httpx.AsyncClient(timeout=30) as client,
        MydaySession(
            client,
            session_id=os.environ["MYDAY_SESSION_ID"],
            id_token=os.environ["MYDAY_ID_TOKEN"],
            device_code=os.environ["MYDAY_DEVICE_CODE"],
        ) as session,
    ):
        items = await session.get_calendar()
        log.info("calendar: %s", items)
        await asyncio.Event().wait()  # keep session alive; Ctrl+C to stop


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
