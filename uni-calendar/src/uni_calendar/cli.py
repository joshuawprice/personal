import asyncio
import contextlib
import html
import json
import logging
import os
import re
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import date, datetime, time as dtime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

import httpx2
import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from .myday_session import MydaySession

BASE = "https://api.myday.cloud/legacy/api/aggregate/v2/calendaritem"

# Local timezone used for "today", "6pm" and for displaying times.
LOCAL_TZ = ZoneInfo(os.environ.get("TIMETABLE_TZ", "Europe/London"))
# After this local time, today is considered finished.
DAY_CUTOFF = dtime(18, 0)
# How many days of calendar to fetch, starting from the first shown day.
DAYS_AHEAD = int(os.environ.get("TIMETABLE_DAYS_AHEAD", "14"))
# Show times as 13:00 instead of 1:00 PM.
TIME_24H = os.environ.get("TIMETABLE_24H") == "1"
# Max time the scheduler sleeps between checks.
CHECK_INTERVAL = 60
# Minimum delay between retries after a failed fetch.
RETRY_INTERVAL = 300
# Upper bound on how long a browser waits before reloading the page.
PAGE_REFRESH_MAX = 30 * 60

COLORS = ["#2563eb", "#16a34a", "#d97706", "#db2777", "#7c3aed", "#0891b2"]

log = logging.getLogger(__name__)

TEMPLATES = Environment(
    loader=FileSystemLoader(Path(__file__).parent),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Event:
    start: datetime  # aware, UTC
    end: datetime  # aware, UTC
    subject: str
    location: str
    categories: tuple[str, ...]
    body: Markup  # sanitised HTML
    search_text: str  # lower-cased text used by the search box

    @property
    def local_start(self) -> datetime:
        return self.start.astimezone(LOCAL_TZ)

    @property
    def local_end(self) -> datetime:
        return self.end.astimezone(LOCAL_TZ)


@dataclass
class CalendarCache:
    window_start: datetime | None = None
    window_end: datetime | None = None
    events: list[Event] | None = None
    colors: dict[str, str] = field(default_factory=dict)
    fetched_at: datetime | None = None
    last_attempt: float = 0.0  # time.monotonic()
    last_error: str | None = None


_cache = CalendarCache()


# --------------------------------------------------------------------------- #
# Time helpers
# --------------------------------------------------------------------------- #


def desired_window(now: datetime | None = None) -> tuple[datetime, datetime]:
    """[start, end) window to show: from today, or from tomorrow after 18:00."""
    now = now or datetime.now(LOCAL_TZ)
    first_day = now.date()
    if now.time() >= DAY_CUTOFF:
        first_day += timedelta(days=1)

    start = datetime.combine(first_day, dtime.min, tzinfo=LOCAL_TZ)
    end = datetime.combine(
        first_day + timedelta(days=DAYS_AHEAD), dtime.min, tzinfo=LOCAL_TZ
    )
    return start, end


def seconds_until_next_boundary(now: datetime | None = None) -> float:
    """Seconds until the next 18:00 cutoff or midnight, whichever comes first."""
    now = now or datetime.now(LOCAL_TZ)
    boundaries = [
        datetime.combine(now.date() + timedelta(days=1), dtime.min, tzinfo=LOCAL_TZ)
    ]
    cutoff = datetime.combine(now.date(), DAY_CUTOFF, tzinfo=LOCAL_TZ)
    if now < cutoff:
        boundaries.append(cutoff)
    nxt = min(boundaries)
    # Subtract in UTC: subtracting datetimes that share a tzinfo ignores DST shifts.
    delta = nxt.astimezone(timezone.utc) - now.astimezone(timezone.utc)
    return max(0.0, delta.total_seconds())


def to_api_ts(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


_EXTRA_FRACTION = re.compile(r"(\.\d{6})\d+")


def parse_ts(value: str) -> datetime:
    s = _EXTRA_FRACTION.sub(r"\1", value.strip())
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        # Matches the old browser behaviour: offset-less times are local.
        dt = dt.replace(tzinfo=LOCAL_TZ)
    return dt.astimezone(timezone.utc)


def fmt_time(dt: datetime) -> str:
    if TIME_24H:
        return f"{dt:%H:%M}"
    return f"{dt.hour % 12 or 12}:{dt.minute:02d} {'AM' if dt.hour < 12 else 'PM'}"


def fmt_long_date(d: date) -> str:
    return f"{d:%A} {d.day} {d:%B %Y}"


def fmt_short_date(d: date) -> str:
    return f"{d:%a} {d.day} {d:%b}"


# --------------------------------------------------------------------------- #
# Parsing / sanitising
# --------------------------------------------------------------------------- #


class _BodySanitizer(HTMLParser):
    """Keep only text, <br> and mailto: links from the API's HTML body."""

    _SKIP = {"script", "style", "head", "title"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html: list[str] = []
        self.text: list[str] = []
        self._links: list[bool] = []  # stack: was this <a> emitted?
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip += 1
        elif tag == "br":
            self.html.append("<br>")
            self.text.append(" ")
        elif tag == "a":
            href = (dict(attrs).get("href") or "").strip()
            keep = href.lower().startswith("mailto:")
            self._links.append(keep)
            if keep:
                self.html.append(f'<a href="{html.escape(href, quote=True)}">')

    def handle_endtag(self, tag):
        if tag in self._SKIP:
            self._skip = max(0, self._skip - 1)
        elif tag == "a" and self._links:
            if self._links.pop():
                self.html.append("</a>")

    def handle_data(self, data):
        if not self._skip:
            self.html.append(html.escape(data))
            self.text.append(data)

    def result(self) -> tuple[Markup, str]:
        self.html.extend("</a>" for keep in self._links if keep)
        self._links.clear()
        return Markup("".join(self.html).strip()), " ".join("".join(self.text).split())


def sanitize_body(raw: str | None) -> tuple[Markup, str]:
    parser = _BodySanitizer()
    parser.feed(raw or "")
    parser.close()
    return parser.result()


def parse_events(payload: bytes) -> list[Event]:
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("Unexpected calendar response shape")

    events: list[Event] = []
    for item in data.get("results") or []:
        if not isinstance(item, dict):
            continue
        try:
            start, end = parse_ts(item["Start"]), parse_ts(item["End"])
        except (KeyError, TypeError, ValueError):
            log.warning("Skipping item with bad Start/End: %r", item.get("Subject"))
            continue

        subject = str(item.get("Subject") or "(no title)")
        location = str(item.get("Location") or "")
        categories = tuple(str(c) for c in (item.get("Categories") or []))
        body, body_text = sanitize_body(item.get("Body"))

        events.append(
            Event(
                start=start,
                end=end,
                subject=subject,
                location=location,
                categories=categories,
                body=body,
                search_text=" ".join(
                    [subject, location, *categories, body_text]
                ).lower(),
            )
        )

    events.sort(key=lambda e: e.start)
    return events


# --------------------------------------------------------------------------- #
# Fetching / scheduling
# --------------------------------------------------------------------------- #


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

    if _cache.events is not None and _cache.window_start == start:
        return  # already have the right day's data

    if (
        _cache.last_error is not None
        and time.monotonic() - _cache.last_attempt < RETRY_INTERVAL
    ):
        return  # back off after a failure

    _cache.last_attempt = time.monotonic()
    log.info("Fetching calendar %s -> %s", start.isoformat(), end.isoformat())

    try:
        events = parse_events(await fetch_items(app, start, end))
    except (httpx2.HTTPError, ValueError) as ex:
        _cache.last_error = str(ex) or type(ex).__name__
        log.warning("Calendar fetch failed: %s", _cache.last_error)
        return

    subjects = sorted({e.subject for e in events})
    _cache.colors = {s: COLORS[i % len(COLORS)] for i, s in enumerate(subjects)}
    _cache.window_start = start
    _cache.window_end = end
    _cache.events = events
    _cache.fetched_at = datetime.now(timezone.utc)
    _cache.last_error = None
    log.info("Calendar updated (%d events)", len(events))


async def scheduler(app: FastAPI) -> None:
    while True:
        try:
            await refresh_if_needed(app)
        except Exception:
            log.exception("Unexpected error in calendar scheduler")
        # Wake up right after 18:00 so the new window is fetched promptly.
        await asyncio.sleep(min(CHECK_INTERVAL, seconds_until_next_boundary() + 1))


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
    openapi_url=None,
    lifespan=lifespan,
)


# --------------------------------------------------------------------------- #
# Page
# --------------------------------------------------------------------------- #

NO_CACHE = {"Cache-Control": "no-cache"}


@app.get("/", response_class=HTMLResponse)
async def index(
    module: str = Query("", max_length=200),
    q: str = Query("", max_length=200),
):
    # Only filters are accepted; the time range is always chosen by the server.
    template = TEMPLATES.get_template("index.html")
    now = datetime.now(LOCAL_TZ)

    if _cache.events is None:
        page = template.render(
            loaded=False,
            error=_cache.last_error,
            refresh_seconds=60,
            module="",
            q=q,
            modules=[],
            days=[],
        )
        return HTMLResponse(page, status_code=503, headers=NO_CACHE)

    desired_start, _ = desired_window(now)
    pending = _cache.window_start != desired_start  # 6pm refresh not done yet
    failed = pending and _cache.last_error is not None

    # Hide finished days even if the 6pm refresh hasn't succeeded yet.
    show_from = max(_cache.window_start, desired_start)
    visible = [e for e in _cache.events if e.end > show_from]

    modules = sorted({e.subject for e in visible})
    if module not in modules:
        module = ""
    needle = q.strip().lower()
    rows = [
        e
        for e in visible
        if (not module or e.subject == module)
        and (not needle or needle in e.search_text)
    ]

    today, tomorrow = now.date(), now.date() + timedelta(days=1)
    days: list[dict] = []
    for e in rows:
        d = e.local_start.date()
        if not days or days[-1]["date"] != d:
            suffix = (
                " (today)" if d == today else " (tomorrow)" if d == tomorrow else ""
            )
            days.append(
                {
                    "date": d,
                    "title": fmt_long_date(d) + suffix,
                    "is_today": d == today,
                    "events": [],
                }
            )
        days[-1]["events"].append(
            {
                "time": f"{fmt_time(e.local_start)} – {fmt_time(e.local_end)}",
                "subject": e.subject,
                "categories": e.categories,
                "location": e.location,
                "body": e.body,
                "color": _cache.colors.get(e.subject, COLORS[0]),
            }
        )

    last_day = _cache.window_end.date() - timedelta(days=1)
    fetched_local = _cache.fetched_at.astimezone(LOCAL_TZ)

    if failed:
        refresh = 60
    elif pending:
        refresh = 15  # the scheduler is fetching right now
    else:
        refresh = int(min(PAGE_REFRESH_MAX, seconds_until_next_boundary(now) + 10))

    page = template.render(
        loaded=True,
        refresh_seconds=refresh,
        modules=modules,
        module=module,
        q=q,
        count=len(rows),
        range_label=f"{fmt_short_date(show_from.date())} – {fmt_short_date(last_day)}",
        updated_label=f"{fetched_local:%a} {fmt_time(fetched_local)}",
        failed=failed,
        error=_cache.last_error if failed else None,
        days=days,
    )
    return HTMLResponse(page, headers=NO_CACHE)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
