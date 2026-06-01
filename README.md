# Hersheypark Burger App

Find the nearest major rides at Hersheypark from where you are on the park map. Live wait times and full closest-ride sorting are planned next.

## Current status

| Feature | Status |
|---------|--------|
| 37 major rides in `data.py` | Done |
| Names match [queue-times.com](https://queue-times.com/parks/15/queue_times.json) | Done |
| REST API (list rides, ride by index, closest stub) | Done |
| Validation scripts + tests | Done |
| Six closest rides by distance (`getclose()` in `hershey.py`) | Not implemented |
| Live wait times | Not implemented |

## Project structure

| File | Purpose |
|------|---------|
| `data.py` | Ride names, map `x`/`y` — **edit rides here** |
| `api.py` | FastAPI app |
| `hershey.py` | Distance / closest-ride logic (work in progress) |
| `tests/` | Tests and checks (`test_api.py`, `check_api.py`, `validate_rides.py`) |
| `apistuff.py` | Local script to print queue-times JSON |
| `vercel.json` | Vercel deploy config |
| `.gitignore` | Ignores `__pycache__`, `.env`, caches, etc. |

## Setup

```powershell
cd Hersheyparkburgerapp
pip install -r requirements.txt
```

For tests:

```powershell
pip install pytest
```

## Run the API locally

```powershell
uvicorn api:app --reload
```

| URL | What |
|-----|------|
| http://127.0.0.1:8000/docs | Interactive API docs (Swagger) |
| http://127.0.0.1:8000/rides | Full ride list |
| http://127.0.0.1:8000/health | Health check |

Stop with **Ctrl+C**.

## How the client should work

1. **`GET /rides`** — show the user a picker (dropdown, buttons, etc.).
2. User picks a ride — your app stores its **`index`** from the response.
3. **`GET /rides/{index}/closest`** — six nearest rides from that location (placeholder until `getclose()` is done).

The server does not remember the user between requests. Pass the **index** in the URL each time.

Example: user picks **Skyrush** (look up its index from `GET /rides`; currently **27** in alphabetical order):

```http
GET /rides/27/closest
```

> Indexes change if you reorder `RIDES` in `data.py`. Always use the `index` field from `/rides`, not a hardcoded number.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/health` | `{"status": "ok"}` |
| GET | `/rides` | All rides: `count`, `names`, `rides[]` |
| GET | `/rides/{index}` | One ride (`index`, `name`, `x`, `y`) |
| GET | `/rides/{index}/closest` | Origin ride + six closest (placeholder) |

Invalid index → **404**.

### `GET /rides` (excerpt)

```json
{
  "count": 37,
  "names": ["Breakers Edge Water Coaster", "Candymonium", ...],
  "rides": [
    { "index": 0, "name": "Breakers Edge Water Coaster", "x": 1960, "y": 1570 },
    { "index": 27, "name": "Skyrush", "x": 3660, "y": 1430 }
  ]
}
```

### `GET /rides/{index}/closest` (excerpt)

```json
{
  "from": { "index": 27, "name": "Skyrush", "x": 3660, "y": 1430 },
  "implemented": false,
  "message": "Closest-ride sorting not implemented yet (see getclose() in hershey.py).",
  "closest_rides": [
    { "rank": 1, "index": null, "name": null, "distance": null, "wait_minutes": null }
  ]
}
```

## Ride data (`data.py`)

Edit the `RIDES` list at the top of `data.py`. Rules:

- **`name`** — must match queue-times.com **exactly** (for future wait times).
- **Major rides only** — coasters, major water rides, towers, monorail, railroad (not kiddie flats).
- **List order** = API index (`0`, `1`, `2`, …).
- **`x` / `y`** — your park map grid; refine new rides on the overlay.

```python
RIDES = [
    {"name": "Skyrush", "x": 3660, "y": 1430},
    ...
]
```

### Three ways the same data is exposed

Everything below is **built from `RIDES`** — edit the list only; do not duplicate coordinates elsewhere.

| Variable | Type | Used by | Purpose |
|----------|------|---------|---------|
| `RIDES` | list of dicts | API (`api.py`) | Ordered rides; **index in this list = API index** |
| `rides` | dict | `hershey.py` | Lookup by name: `rides["Skyrush"]["x"]` |
| `RIDE_NAMES` | list of strings | Convenience | All names in order |
| `RIDE_COUNT` | int | API | `37` — number of rides |

**List (API / frontend):**

```python
RIDES[27]  # -> {"name": "Skyrush", "x": 3660, "y": 1430}
```

**Dict (scripts / lookup by name):**

```python
rides = {
    "Skyrush": {"x": 3660, "y": 1430},
    "Comet": {"x": 3380, "y": 1570},
    ...
}
rides["Skyrush"]["y"]  # -> 1430
```

The line that builds `rides` from `RIDES`:

```python
rides = {ride["name"]: {"x": ride["x"], "y": ride["y"]} for ride in RIDES}
```

See the comment block at the **bottom of `data.py`** for a longer explanation.

## Verify data and API

Run after editing `data.py`:

```powershell
python tests/validate_rides.py
python tests/check_api.py
pytest tests/ -q
```

| Command | Checks |
|---------|--------|
| `tests/validate_rides.py` | Names vs live queue-times API; no duplicate/bad coordinates; prints coordinate table |
| `tests/check_api.py` | Every index works on `/rides/{index}` |
| `pytest tests/` | Full API test suite (78 tests) |

**Names** can be verified automatically. **Coordinates** need a manual pass on your map overlay after automated sanity checks pass — there is no public API for ride positions.

## Deploy on Vercel

1. Push to GitHub.
2. Import the repo at [vercel.com](https://vercel.com).
3. Deploy (uses `vercel.json` + `requirements.txt`).

Live URLs: `https://your-project.vercel.app/rides`, `/docs`, etc.

## CLI (`hershey.py`)

```powershell
python hershey.py
```

Separate from the web API. `getclose()` is unfinished. Ride names in `data.py` match queue-times (e.g. `sooperdooperLooper`), so typed input may not match until the CLI uses ride **index** like the API.

## Next steps (code)

1. Implement `getclose()` in `hershey.py` using `getcords()` and `getdistance()`.
2. Call that logic from `GET /rides/{index}/closest` in `api.py`.
3. Add wait times via `QUEUE_TIMES_URL` in `data.py` (see `apistuff.py`).
