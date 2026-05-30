"""
Quick manual check — prints pass/fail for every ride index (no pytest required).

Run:
    python check_api.py
"""

from fastapi.testclient import TestClient

from api import app
from data import RIDE_NAMES, rides

client = TestClient(app)
failed = []


def ok(label: str) -> None:
    print(f"  OK  {label}")


def fail(label: str, detail: str) -> None:
    print(f"  FAIL  {label} — {detail}")
    failed.append(label)


print(f"Checking {len(RIDE_NAMES)} rides...\n")

for index, name in enumerate(RIDE_NAMES):
    response = client.get(f"/rides/{index}")
    if response.status_code != 200:
        fail(name, f"GET /rides/{index} -> {response.status_code}")
        continue

    data = response.json()
    if data["name"] != name or data["x"] != rides[name]["x"] or data["y"] != rides[name]["y"]:
        fail(name, "response mismatch")
        continue

    ok(f"[{index}] {name}")

print()
if failed:
    print(f"FAILED: {len(failed)} ride(s)")
    raise SystemExit(1)

print("All rides match.")
