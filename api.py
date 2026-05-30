"""
Hersheypark API — basic endpoints for rides and health checks.

Run locally:
    pip install -r requirements.txt
    uvicorn api:app --reload

Deploy on Vercel: connect this repo; Vercel uses vercel.json + this file.

Clients should call GET /rides, show the user the list, then request by index
(e.g. GET /rides/0) — no string matching on user input.
"""

from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query

from data import QUEUE_TIMES_URL, RIDE_COUNT, RIDE_NAMES, RIDES

app = FastAPI(
    title="Hersheypark API",
    description="Simple API for Hersheypark ride data.",
    version="0.1.0",
)


def _ride_payload(index: int) -> dict[str, Any]:
    ride = RIDES[index]
    return {
        "index": index,
        "name": ride["name"],
        "x": ride["x"],
        "y": ride["y"],
    }


@app.get("/")
def root():
    return {
        "name": "Hersheypark API",
        "endpoints": ["/health", "/rides", "/rides/{index}", "/wait-times"],
        "docs": "/docs",
        "note": "GET /rides for the list; use index from that response (e.g. /rides/0).",
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


@app.get("/wait-times")
def wait_times(index: Optional[int] = Query(default=None, description="Ride index from GET /rides")):
    """Placeholder for live wait times (see apistuff.py for queue-times.com integration)."""
    payload = {
        "source": QUEUE_TIMES_URL,
        "message": "Connect queue-times or Hersheypark data here.",
        "rides_available": RIDE_COUNT,
    }
    if index is not None:
        if index < 0 or index >= RIDE_COUNT:
            raise HTTPException(
                status_code=404,
                detail=f"Invalid index {index}. Use 0 to {RIDE_COUNT - 1} from GET /rides.",
            )
        payload["ride"] = _ride_payload(index)
    return payload
