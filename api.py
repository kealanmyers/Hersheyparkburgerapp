"""
Hersheypark API — basic endpoints for rides and health checks.

Run locally:
    pip install -r requirements.txt
    uvicorn api:app --reload

Deploy on Vercel: connect this repo; Vercel uses vercel.json + this file.

Clients should call GET /rides, show the user the list, then request by index
(e.g. GET /rides/0) — no string matching on user input.
"""

from typing import Any

from fastapi import FastAPI, HTTPException

from data import RIDE_COUNT, RIDE_NAMES, RIDES

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


def _placeholder_closest_rides() -> list[dict[str, Any]]:
    """Placeholder until getclose() in hershey.py is implemented."""
    
    return [
        {
            "rank": rank,
            "index": None,
            "name": None,
            "distance": None,
            "wait_minutes": None,
        }
        for rank in range(1, 7)
    ]


@app.get("/")
def root():
    return {
        "name": "Hersheypark API",
        "endpoints": ["/health", "/rides", "/rides/{index}", "/rides/{index}/closest"],
        "docs": "/docs",
        "note": "GET /rides for the list; use index from that response (e.g. /rides/0/closest).",
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
def closest_rides(from_index: int):
    """
    Six closest rides to the ride at from_index (user's current location).

    Real logic will call getclose() in hershey.py once implemented.
    """
    if from_index < 0 or from_index >= RIDE_COUNT:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid index {from_index}. Use 0 to {RIDE_COUNT - 1} from GET /rides.",
        )
    return {
        "from": _ride_payload(from_index),
        "implemented": False,
        "message": "Closest-ride sorting not implemented yet (see getclose() in hershey.py).",
        "closest_rides": _placeholder_closest_rides(),
    }
