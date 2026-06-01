"""
Validate ride names (queue-times.com) and coordinate sanity (data.py).

Names: checked against the live queue-times API.
Coordinates: no public API — we flag duplicates, (0,0), and outliers;
  you must confirm positions on your park map grid by hand.

Run from project root:
    python tests/validate_rides.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data import QUEUE_TIMES_URL, RIDES, RIDE_NAMES

HEADERS = {"User-Agent": "Hersheyparkburgerapp/1.0"}

# Adjust if your map grid range changes (from current ride spread).
MAP_X_MIN, MAP_X_MAX = 1000, 4500
MAP_Y_MIN, MAP_Y_MAX = 500, 2800


def _norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def validate_names() -> bool:
    print("=== Names (queue-times.com) ===\n")
    response = requests.get(QUEUE_TIMES_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()

    api_names: list[str] = []
    for land in response.json().get("lands", []):
        for ride in land.get("rides", []):
            api_names.append(ride["name"].strip())

    api_exact = set(api_names)
    ok = True

    for name in RIDE_NAMES:
        if name in api_exact:
            print(f"  OK   {name}")
        else:
            print(f"  FAIL {name!r} — not found on queue-times (check spelling/capitalization)")
            ok = False

    if ok:
        print(f"\nAll {len(RIDE_NAMES)} names match the API.\n")
    else:
        print("\nFix failed names in data.py so they match the API exactly.\n")
    return ok


def validate_coordinates() -> bool:
    print("=== Coordinates (sanity checks) ===\n")
    ok = True

    # (0, 0) — usually means "not placed on map yet"
    at_origin = [r["name"] for r in RIDES if r["x"] == 0 and r["y"] == 0]
    if at_origin:
        ok = False
        print("  FAIL rides still at (0, 0) — set map coordinates:")
        for name in at_origin:
            print(f"       - {name}")
        print()

    # Out of expected grid range
    out_of_range = []
    for r in RIDES:
        if not (MAP_X_MIN <= r["x"] <= MAP_X_MAX and MAP_Y_MIN <= r["y"] <= MAP_Y_MAX):
            out_of_range.append(r["name"])
    if out_of_range:
        ok = False
        print(f"  FAIL outside grid range x=[{MAP_X_MIN},{MAP_X_MAX}] y=[{MAP_Y_MIN},{MAP_Y_MAX}]:")
        for name in out_of_range:
            ride = next(x for x in RIDES if x["name"] == name)
            print(f"       - {name}: ({ride['x']}, {ride['y']})")
        print()

    # Duplicate (x, y) — two rides cannot share the same map point
    by_pos: dict[tuple[int, int], list[str]] = defaultdict(list)
    for r in RIDES:
        by_pos[(r["x"], r["y"])].append(r["name"])

    duplicates = {pos: names for pos, names in by_pos.items() if len(names) > 1}
    if duplicates:
        ok = False
        print("  FAIL duplicate coordinates (same x, y for multiple rides):")
        for (x, y), names in sorted(duplicates.items()):
            print(f"       ({x}, {y}): {', '.join(names)}")
        print()

    # Very close pairs — might be intentional (e.g. triple tower) but worth reviewing
    close_pairs: list[tuple[str, str, float]] = []
    for i, a in enumerate(RIDES):
        for b in RIDES[i + 1 :]:
            dx = a["x"] - b["x"]
            dy = a["y"] - b["y"]
            dist = (dx * dx + dy * dy) ** 0.5
            if 0 < dist < 80:
                close_pairs.append((a["name"], b["name"], dist))

    if close_pairs:
        print("  WARN rides very close on map (< 80 units) — verify on your grid:")
        for a, b, dist in sorted(close_pairs, key=lambda t: t[2]):
            print(f"       {a} <-> {b}  ({dist:.0f} units)")
        print()

    if ok and not at_origin and not out_of_range and not duplicates:
        print("  OK   no (0,0), out-of-range, or duplicate coordinates.")
        print()
        print("  Manual step: open your park map overlay and confirm each")
        print("  (x, y) is on the correct ride. Automated checks cannot do that.\n")

    return ok


def print_coordinate_table() -> None:
    print("=== Coordinate table (for map review) ===\n")
    print(f"{'index':>5}  {'x':>5}  {'y':>5}  name")
    print("-" * 60)
    for i, r in enumerate(RIDES):
        print(f"{i:>5}  {r['x']:>5}  {r['y']:>5}  {r['name']}")
    print()


def main() -> None:
    names_ok = validate_names()
    coords_ok = validate_coordinates()
    print_coordinate_table()

    if names_ok and coords_ok:
        print("Validation passed (names + coordinate sanity).")
        print("Still review coordinates on your map if you changed or added rides.")
        return

    print("Validation failed — fix issues above.")
    sys.exit(1)


if __name__ == "__main__":
    main()
