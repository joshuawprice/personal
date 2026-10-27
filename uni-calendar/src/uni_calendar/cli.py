import asyncio
import logging
import os
import time
from pathlib import Path
from urllib.parse import quote

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, Response

from .myday_session import MydaySession

TS_PATTERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
CACHE_TTL = 60

BASE = "https://api.myday.cloud/legacy/api/aggregate/v2/calendaritem"

log = logging.getLogger(__name__)

HTML = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")

app = FastAPI(title="Uni Timetable", docs_url=None, redoc_url=None)

_cache: dict[tuple[str, str], tuple[float, bytes]] = {}


@app.on_event("startup")
async def startup() -> None:
    client = httpx.AsyncClient(
        timeout=httpx.Timeout(30.0),
    )

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


@app.on_event("shutdown")
async def shutdown() -> None:
    session = app.state.session
    client = app.state.client

    await session.__aexit__(None, None, None)
    await client.aclose()


async def fetch_items(start: str, end: str) -> bytes:
    key = (start, end)

    cached = _cache.get(key)
    if cached and time.monotonic() - cached[0] < CACHE_TTL:
        return cached[1]

    flt = f"End gt datetime'{start}' and Start lt datetime'{end}'"

    url = f"{BASE}?$filter={quote(flt, safe=':')}"

    client: httpx.AsyncClient = app.state.client

    response = await client.get(url)
    response.raise_for_status()

    data = response.content

    _cache[key] = (time.monotonic(), data)

    return data


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML


@app.get("/api/calendar")
async def calendar(
    start: str = Query(..., pattern=TS_PATTERN),
    end: str = Query(..., pattern=TS_PATTERN),
):
    try:
        payload = await fetch_items(start, end)
        return Response(payload, media_type="application/json")

    except httpx.HTTPStatusError as ex:
        raise HTTPException(
            status_code=ex.response.status_code,
            detail=f"Upstream error: {ex.response.reason_phrase}",
        ) from ex

    except httpx.HTTPError as ex:
        raise HTTPException(
            status_code=502,
            detail=str(ex),
        ) from ex


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    main()