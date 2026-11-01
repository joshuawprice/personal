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
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

import hashlib
from collections import Counter
from fastapi.responses import HTMLResponse, Response  # extend existing import


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
        self._links: list[bool] = []  # stack: was this <a> emitted?
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self._SKIP:
            self._skip += 1
        elif tag == "br":
            self.html.append("<br>")
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

    def result(self) -> Markup:
        self.html.extend("</a>" for keep in self._links if keep)
        self._links.clear()
        return Markup("".join(self.html).strip())


def sanitize_body(raw: str | None) -> Markup:
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

        events.append(
            Event(
                start=start,
                end=end,
                subject=str(item.get("Subject") or "(no title)"),
                location=str(item.get("Location") or ""),
                categories=tuple(str(c) for c in (item.get("Categories") or [])),
                body=sanitize_body(item.get("Body")),
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
async def index():
    # No parameters: every visitor gets the same server-chosen timetable.
    template = TEMPLATES.get_template("index.html")
    now = datetime.now(LOCAL_TZ)

    if _cache.events is None:
        page = template.render(
            loaded=False,
            error=_cache.last_error,
            refresh_seconds=60,
            days=[],
        )
        return HTMLResponse(page, status_code=503, headers=NO_CACHE)

    desired_start, _ = desired_window(now)
    pending = _cache.window_start != desired_start  # 6pm refresh not done yet
    failed = pending and _cache.last_error is not None

    # Hide finished days even if the 6pm refresh hasn't succeeded yet.
    show_from = max(_cache.window_start, desired_start)
    visible = [e for e in _cache.events if e.end > show_from]

    today, tomorrow = now.date(), now.date() + timedelta(days=1)
    days: list[dict] = []
    for e in visible:
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
        count=len(visible),
        range_label=f"{fmt_short_date(show_from.date())} – {fmt_short_date(last_day)}",
        updated_label=f"{fetched_local:%a} {fmt_time(fetched_local)}",
        failed=failed,
        error=_cache.last_error if failed else None,
        days=days,
    )
    return HTMLResponse(page, headers=NO_CACHE)

# --------------------------------------------------------------------------- #
# iCalendar feed
# --------------------------------------------------------------------------- #

_BR = re.compile(r"<br\s*/?>", re.I)
_TAG = re.compile(r"<[^>]+>")


def _ics_text(value: str) -> str:
    """Escape a TEXT value per RFC 5545 §3.3.11."""
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", "\\n")
    )


def _ics_fold(line: str) -> str:
    """Fold to <=75 octets per line without splitting multibyte characters."""
    if len(line.encode()) <= 75:
        return line
    parts: list[str] = []
    cur: list[str] = []
    size, limit = 0, 75
    for ch in line:
        n = len(ch.encode())
        if size + n > limit:
            parts.append("".join(cur))
            cur, size, limit = [ch], n, 74  # continuation lines start with a space
        else:
            cur.append(ch)
            size += n
    parts.append("".join(cur))
    return "\r\n ".join(parts)


def _ics_dt(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _body_to_text(body: str) -> str:
    return html.unescape(_TAG.sub("", _BR.sub("\n", str(body)))).strip()


def build_ics(events: list[Event], stamp: datetime) -> str:
    dtstamp = _ics_dt(stamp)
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Uni Timetable//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Uni Timetable",
        f"X-WR-TIMEZONE:{LOCAL_TZ.key}",
        "REFRESH-INTERVAL;VALUE=DURATION:PT1H",
        "X-PUBLISHED-TTL:PT1H",
    ]

    seen: Counter[str] = Counter()
    for e in events:
        key = f"{_ics_dt(e.start)}|{_ics_dt(e.end)}|{e.subject}|{e.location}"
        digest = hashlib.sha1(key.encode()).hexdigest()
        seen[digest] += 1  # disambiguate genuinely identical events
        uid = f"{digest}-{seen[digest]}@uni-timetable"

        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{dtstamp}",
            f"DTSTART:{_ics_dt(e.start)}",
            f"DTEND:{_ics_dt(e.end)}",
            f"SUMMARY:{_ics_text(e.subject)}",
        ]
        if e.location:
            lines.append(f"LOCATION:{_ics_text(e.location)}")
        if description := _body_to_text(e.body):
            lines.append(f"DESCRIPTION:{_ics_text(description)}")
        if e.categories:
            lines.append("CATEGORIES:" + ",".join(_ics_text(c) for c in e.categories))
        lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")
    return "\r\n".join(_ics_fold(l) for l in lines) + "\r\n"


@app.get("/calendar.ics")
async def calendar_ics():
    if _cache.events is None:
        return Response(
            "Calendar not loaded yet\n",
            status_code=503,
            media_type="text/plain",
            headers={**NO_CACHE, "Retry-After": "60"},
        )

    body = build_ics(_cache.events, _cache.fetched_at or datetime.now(timezone.utc))
    return Response(
        body,
        media_type="text/calendar; charset=utf-8",
        headers={
            **NO_CACHE,
            "Content-Disposition": 'inline; filename="timetable.ics"',
        },
    )


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
