"""
export MYDAY_TOKEN='your-token'
python app.py            # UI at http://localhost:8000
python app.py --print    # fetch and print JSON for the default range
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, Response

TOKEN = os.environ.get("MYDAY_TOKEN", "")
BASE = "https://api.myday.cloud/legacy/api/aggregate/v2/calendaritem"
TS_PATTERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
CACHE_TTL = 60  # seconds

session = requests.Session()
session.headers["Authorization"] = f"Bearer {TOKEN}"
_cache: dict[tuple[str, str], tuple[float, bytes]] = {}


def fetch_items(start: str, end: str) -> bytes:
    """start/end: UTC timestamps like 2026-09-28T00:00:00Z. Returns raw JSON bytes."""
    key = (start, end)
    hit = _cache.get(key)
    if hit and time.monotonic() - hit[0] < CACHE_TTL:
        return hit[1]
    flt = f"End gt datetime'{start}' and Start lt datetime'{end}'"
    # Build the URL by hand: `params=` would encode spaces as '+', which OData servers may reject.
    r = session.get(f"{BASE}?$filter={quote(flt, safe=':')}", timeout=30)
    r.raise_for_status()
    _cache[key] = (time.monotonic(), r.content)
    return r.content


HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")

app = FastAPI(title="My Timetable", docs_url=None, redoc_url=None)


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML


@app.get("/api/calendar")
def calendar(
    start: str = Query(..., pattern=TS_PATTERN),
    end: str = Query(..., pattern=TS_PATTERN),
):
    try:
        return Response(fetch_items(start, end), media_type="application/json")
    except requests.HTTPError as ex:
        raise HTTPException(
            ex.response.status_code, f"Upstream error: {ex.response.reason}"
        )
    except requests.RequestException as ex:
        raise HTTPException(502, str(ex))


def main():
    if not TOKEN:
        sys.exit("Set MYDAY_TOKEN environment variable first.")
    if "--print" in sys.argv:
        fmt = "%Y-%m-%dT%H:%M:%SZ"
        t0 = datetime.now(datetime.UTC).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        print(
            json.dumps(
                json.loads(
                    fetch_items(
                        t0.strftime(fmt), (t0 + timedelta(days=42)).strftime(fmt)
                    )
                ),
                indent=2,
            )
        )
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
