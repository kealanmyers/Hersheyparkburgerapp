"""
Hersheypark API — basic endpoints for rides and health checks.

Run locally:
    pip install -r requirements.txt
    uvicorn api:app --reload

Deploy on Vercel: connect this repo; Vercel uses vercel.json + this file.

Clients should call GET /rides, show the user the list, then request by index
(e.g. GET /rides/0) — no string matching on user input.
"""

import time
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path

from data import QUEUE_TIMES_URL, RIDE_COUNT, RIDE_NAMES, RIDES

app = FastAPI(
    title="Hersheypark API",
    description="Simple API for Hersheypark ride data.",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# queue-times wait-time cache (avoid hitting upstream on every request)
# ---------------------------------------------------------------------------

_WAIT_CACHE_TTL_SECONDS = 60
_wait_cache: dict[str, Any] = {"fetched_at": 0.0, "lookup": {}}


async def _get_wait_lookup() -> dict[str, dict[str, Any]]:
    """
    Returns a dict keyed by exact ride name (lowercased) -> ride payload from queue-times.
    Cached in-memory for a short TTL.
    """
    now = time.time()
    fetched_at = float(_wait_cache.get("fetched_at") or 0.0)
    if (now - fetched_at) < _WAIT_CACHE_TTL_SECONDS and isinstance(_wait_cache.get("lookup"), dict):
        return _wait_cache["lookup"]

    headers = {"User-Agent": "Hersheyparkburgerapp/1.0"}
    async with httpx.AsyncClient(timeout=15.0, headers=headers) as client:
        resp = await client.get(QUEUE_TIMES_URL)
        resp.raise_for_status()
        data = resp.json()

    lookup: dict[str, dict[str, Any]] = {}
    for land in data.get("lands", []):
        for ride in land.get("rides", []):
            name = (ride.get("name") or "").strip()
            if name:
                lookup[name.lower()] = ride

    _wait_cache["fetched_at"] = now
    _wait_cache["lookup"] = lookup
    return lookup


def _ride_payload(index: int) -> dict[str, Any]:
    ride = RIDES[index]
    return {
        "index": index,
        "name": ride["name"],
        "x": ride["x"],
        "y": ride["y"],
    }

def _distance(a: dict[str, Any], b: dict[str, Any]) -> float:
    dx = float(a["x"]) - float(b["x"])
    dy = float(a["y"]) - float(b["y"])
    return (dx * dx + dy * dy) ** 0.5


@app.get("/", response_class=HTMLResponse)
def single_page():
    html_path = Path(__file__).resolve().parent / "web" / "index.html"
    html = html_path.read_text(encoding="utf-8")
    return HTMLResponse(html)


@app.get("/api")
def api_info():
    return {
        "name": "Hersheypark API",
        "endpoints": ["/", "/api", "/health", "/rides", "/rides/{index}", "/rides/{index}/closest"],
        "docs": "/docs",
        "note": "Open / for the single-page UI. API clients: GET /rides then /rides/{index}/closest.",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/rides")
def list_rides():
    return {
        "count": RIDE_COUNT,
        "names": RIDE_NAMES,
        "rides": [_ride_payload(i) for i in range(RIDE_COUNT)],
    }


@app.get("/rides/{index}")
def get_ride(index: int):
    if index < 0 or index >= RIDE_COUNT:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid index {index}. Use 0 to {RIDE_COUNT - 1} from GET /rides.",
        )
    return _ride_payload(index)


@app.get("/rides/{from_index}/closest")
async def closest_rides(from_index: int):
    """
    Six closest rides to the ride at from_index (user's current location).
    """
    if from_index < 0 or from_index >= RIDE_COUNT:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid index {from_index}. Use 0 to {RIDE_COUNT - 1} from GET /rides.",
        )

    origin = _ride_payload(from_index)
    wait_lookup = await _get_wait_lookup()

    candidates: list[dict[str, Any]] = []
    for idx in range(RIDE_COUNT):
        if idx == from_index:
            continue
        ride = _ride_payload(idx)
        dist = _distance(origin, ride)
        wait = wait_lookup.get(ride["name"].lower(), {})
        wait_minutes = wait.get("wait_time")
        candidates.append(
            {
                "index": idx,
                "name": ride["name"],
                "distance": dist,
                "wait_minutes": wait_minutes,
            }
        )

    candidates.sort(key=lambda x: x["distance"])
    top = candidates[:6]
    closest = [
        {
            "rank": i + 1,
            "index": item["index"],
            "name": item["name"],
            "distance": item["distance"],
            "wait_minutes": item["wait_minutes"],
        }
        for i, item in enumerate(top)
    ]

    return {"from": origin, "implemented": True, "closest_rides": closest}
