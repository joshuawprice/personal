import asyncio
import contextlib
import logging
import os
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from datetime import time as dtime
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

import httpx2
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response

from .myday_session import MydaySession

BASE = "https://api.myday.cloud/legacy/api/aggregate/v2/calendaritem"

# Local timezone used to decide what "today" and "6pm" mean.
LOCAL_TZ = ZoneInfo(os.environ.get("TIMETABLE_TZ", "Europe/London"))
# After this local time, today is considered finished.
DAY_CUTOFF = dtime(18, 0)
# How many days of calendar to fetch, starting from the first shown day.
DAYS_AHEAD = int(os.environ.get("TIMETABLE_DAYS_AHEAD", "14"))
# How often the scheduler wakes up to check whether a refresh is due.
CHECK_INTERVAL = 60
# Minimum delay between retries after a failed fetch.
RETRY_INTERVAL = 300

log = logging.getLogger(__name__)

HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")


@dataclass
class CalendarCache:
    window_start: datetime | None = None
    window_end: datetime | None = None
    payload: bytes | None = None
    fetched_at: datetime | None = None
    last_attempt: float = 0.0  # time.monotonic()
    last_error: str | None = None


_cache = CalendarCache()


def desired_window(now: datetime | None = None) -> tuple[datetime, datetime]:
    """Return the [start, end) window that should currently be shown.

    Before 18:00 local time the window starts at today's midnight;
    from 18:00 onwards it starts at tomorrow's midnight.
    """
    now = now or datetime.now(LOCAL_TZ)
    first_day = now.date()
    if now.time() >= DAY_CUTOFF:
        first_day += timedelta(days=1)

    start = datetime.combine(first_day, dtime.min, tzinfo=LOCAL_TZ)
    end = datetime.combine(
        first_day + timedelta(days=DAYS_AHEAD), dtime.min, tzinfo=LOCAL_TZ
    )
    return start, end


def to_api_ts(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


async def fetch_items(app: FastAPI, start: datetime, end: datetime) -> bytes:
    flt = f"End gt datetime'{to_api_ts(start)}' and Start lt datetime'{to_api_ts(end)}'"
    url = f"{BASE}?$filter={quote(flt, safe=':')}"

    client: httpx2.AsyncClient = app.state.client
    session: MydaySession = app.state.session

    access_token = session.access_token
    if not access_token:
        raise httpx2.HTTPError("MyDay session has no access code")

    response = await client.get(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    response.raise_for_status()
    return response.content


async def refresh_if_needed(app: FastAPI) -> None:
    start, end = desired_window()

    if _cache.payload is not None and _cache.window_start == start:
        return  # already have the right day's data

    if (
        _cache.last_error is not None
        and time.monotonic() - _cache.last_attempt < RETRY_INTERVAL
    ):
        return  # back off after a failure

    _cache.last_attempt = time.monotonic()
    log.info("Fetching calendar %s -> %s", start.isoformat(), end.isoformat())

    try:
        payload = await fetch_items(app, start, end)
    except httpx2.HTTPError as ex:
        _cache.last_error = str(ex) or type(ex).__name__
        log.warning("Calendar fetch failed: %s", _cache.last_error)
        return

    _cache.window_start = start
    _cache.window_end = end
    _cache.payload = payload
    _cache.fetched_at = datetime.now(timezone.utc)
    _cache.last_error = None
    log.info("Calendar updated (%d bytes)", len(payload))


async def scheduler(app: FastAPI) -> None:
    while True:
        try:
            await refresh_if_needed(app)
        except Exception:
            log.exception("Unexpected error in calendar scheduler")
        await asyncio.sleep(CHECK_INTERVAL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = httpx2.AsyncClient(timeout=httpx2.Timeout(30.0))
    session = MydaySession(
        client,
        session_id=os.environ["MYDAY_SESSION_ID"],
        id_token=os.environ["MYDAY_ID_TOKEN"],
        device_code=os.environ["MYDAY_DEVICE_CODE"],
    )
    await session.__aenter__()

    app.state.client = client
    app.state.session = session
    log.info("MyDay session started")

    # Load data before accepting requests; the scheduler takes over afterwards.
    try:
        await refresh_if_needed(app)
    except Exception:
        log.exception("Initial calendar fetch failed")

    task = asyncio.create_task(scheduler(app))
    try:
        yield
    finally:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task
        await session.__aexit__(None, None, None)
        await client.aclose()


app = FastAPI(
    title="Uni Timetable",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML


@app.get("/api/calendar")
async def calendar():
    # No parameters: clients always get the server-chosen window.
    if _cache.payload is None:
        detail = "Calendar not loaded yet"
        if _cache.last_error:
            detail += f" (last error: {_cache.last_error})"
        raise HTTPException(status_code=503, detail=detail)

    desired_start, _ = desired_window()
    headers = {
        "Cache-Control": "no-cache",
        "X-Calendar-Start": to_api_ts(_cache.window_start),
        "X-Calendar-End": to_api_ts(_cache.window_end),
        "X-Calendar-Fetched-At": to_api_ts(_cache.fetched_at),
    }
    if _cache.window_start != desired_start:
        headers["X-Calendar-Stale"] = "true"  # 6pm refresh hasn't succeeded yet

    return Response(_cache.payload, media_type="application/json", headers=headers)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
