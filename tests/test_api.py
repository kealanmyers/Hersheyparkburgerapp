"""
Checks that the ride list and index lookups match data.py.

Run from project root:
    pip install pytest httpx
    pytest tests/ -v
"""

import pytest
from fastapi.testclient import TestClient

from api import app
from data import RIDE_NAMES, RIDES, rides

client = TestClient(app)


def test_ride_names_match_data_file():
    assert RIDE_NAMES == [r["name"] for r in RIDES]
    assert len(rides) == len(RIDES)


def test_list_rides():
    response = client.get("/rides")
    assert response.status_code == 200
    body = response.json()

    assert body["count"] == len(rides)
    assert body["names"] == RIDE_NAMES
    assert len(body["rides"]) == len(rides)

    for i, item in enumerate(body["rides"]):
        name = RIDE_NAMES[i]
        assert item["index"] == i
        assert item["name"] == name
        assert item["x"] == rides[name]["x"]
        assert item["y"] == rides[name]["y"]


@pytest.mark.parametrize("index", range(len(RIDE_NAMES)))
def test_get_ride_by_index(index: int):
    response = client.get(f"/rides/{index}")
    assert response.status_code == 200
    data = response.json()
    name = RIDE_NAMES[index]
    assert data["name"] == name
    assert data["x"] == rides[name]["x"]
    assert data["y"] == rides[name]["y"]


def test_invalid_index_returns_404():
    assert client.get("/rides/999").status_code == 404
    assert client.get("/rides/-1").status_code == 404


def test_closest_rides_returns_six_placeholders():
    skyrush_index = RIDE_NAMES.index("Skyrush")
    response = client.get(f"/rides/{skyrush_index}/closest")
    assert response.status_code == 200
    body = response.json()

    assert body["from"]["name"] == "Skyrush"
    assert body["implemented"] is False
    assert len(body["closest_rides"]) == 6
    assert body["closest_rides"][0]["rank"] == 1
    assert body["closest_rides"][0]["index"] is None


@pytest.mark.parametrize("index", range(len(RIDE_NAMES)))
def test_closest_rides_accepts_every_index(index: int):
    response = client.get(f"/rides/{index}/closest")
    assert response.status_code == 200
    assert response.json()["from"]["index"] == index
