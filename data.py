"""
All Hersheypark constants live here.

- `name` matches queue-times.com exactly (for wait-time API).
- Edit x/y map coordinates on your park grid; new rides use rough placeholders.
- List order = API index (0, 1, 2, ...).
"""

QUEUE_TIMES_URL = "https://queue-times.com/parks/15/queue_times.json"

# Major rides only — names from queue-times.com/parks/15/queue_times.json
RIDES = [
    {"name": "Breakers Edge", "x": 1960, "y": 1570},
    {"name": "Candymonium", "x": 4040, "y": 2210},
    {"name": "Carrousel", "x": 3830, "y": 2390},
    {"name": "Coal Cracker", "x": 3460, "y": 820},
    {"name": "Cocoa Cruiser", "x": 2940, "y": 1730},
    {"name": "Coastline Plunge - Hydro", "x": 1820, "y": 1580},
    {"name": "Coastline Plunge - Pipeline", "x": 1860, "y": 1560},
    {"name": "Coastline Plunge - Riptide", "x": 1900, "y": 1540},
    {"name": "Coastline Plunge - Surge", "x": 1780, "y": 1600},
    {"name": "Coastline Plunge - Vortex", "x": 1740, "y": 1620},
    {"name": "Coastline Plunge - Whirlwind", "x": 1700, "y": 1640},
    {"name": "Comet", "x": 3380, "y": 1570},
    {"name": "Dry Gulch Railroad", "x": 2650, "y": 1350},
    {"name": "East Coast Waterworks", "x": 1880, "y": 1780},
    {"name": "Fahrenheit", "x": 2350, "y": 1380},
    {"name": "Ferris Wheel", "x": 3070, "y": 1560},
    {"name": "Great Bear", "x": 3310, "y": 950},
    {"name": "Hershey Triple Tower - Hershey's Kisses Tower", "x": 3250, "y": 780},
    {"name": "Hershey Triple Tower - Hershey's Tower", "x": 3175, "y": 750},
    {"name": "Hershey Triple Tower - Reese's Tower", "x": 3320, "y": 770},
    {"name": "Intercoastal Waterway", "x": 1650, "y": 1830},
    {"name": "Jolly Rancher Remix", "x": 2210, "y": 1660},
    {"name": "Kissing Tower", "x": 3190, "y": 760},
    {"name": "Lightning Racer", "x": 1230, "y": 2140},
    {"name": "Mix'd Flavored By Jolly Rancher", "x": 2560, "y": 1810},
    {"name": "Monorail", "x": 3600, "y": 2050},
    {"name": "Reese's Cupfusion", "x": 3260, "y": 1810},
    {"name": "Skyrush", "x": 3660, "y": 1430},
    {"name": "sooperdooperLooper", "x": 3820, "y": 1260},
    {"name": "Laff Trakk", "x": 1370, "y": 2630},
    {"name": "Storm Runner", "x": 2420, "y": 1490},
    {"name": "Tidal Force", "x": 2050, "y": 1680},
    {"name": "Trailblazer", "x": 2780, "y": 1480},
    {"name": "Twizzlers Twisted Gravity", "x": 3190, "y": 1340},
    {"name": "Whitecap Racer", "x": 1790, "y": 1650},
    {"name": "Wild Mouse", "x": 1580, "y": 2290},
    {"name": "Wildcat's Revenge", "x": 1900, "y": 2490},
]

# Built from RIDES — use these everywhere else instead of copying data again.
rides = {ride["name"]: {"x": ride["x"], "y": ride["y"]} for ride in RIDES}
RIDE_NAMES = [ride["name"] for ride in RIDES]
RIDE_COUNT = len(RIDES)

# ---------------------------------------------------------------------------
# How `rides` works (dictionary built from the RIDES list above)
# ---------------------------------------------------------------------------
#
# RIDES is a list of dicts, one per ride:
#   [{"name": "Skyrush", "x": 3660, "y": 1430}, ...]
#
# `rides` turns that into a dict keyed by ride name so you can look up coords fast:
#
#   rides = {
#       "Skyrush": {"x": 3660, "y": 1430},
#       "Comet":   {"x": 3380, "y": 1570},
#       ...
#   }
#
# Usage in code (e.g. hershey.py):
#   rides["Skyrush"]["x"]   -> 3660
#   rides["Skyrush"]["y"]   -> 1430
#
# The API uses RIDES + index (0, 1, 2, ...) instead, because the frontend
# picks from a list. Both come from the same data — only the shape differs.
#
# RIDE_NAMES = ["Breakers Edge Water Coaster", "Candymonium", ...]  (ordered list)
# RIDE_COUNT = 37




# rides = {
#     "Candymonium": {"x": 4040, "y": 2210},
#     "Carrousel": {"x": 3830, "y": 2390},


#     "Kissing Tower": {"x": 3190, "y": 760},
#     "Great Bear": {"x": 3310, "y": 950},
#     "Coal Cracker": {"x": 3460, "y": 820},

#     "Trailblazer": {"x": 2780, "y": 1480},
#     "Storm Runner": {"x": 2420, "y": 1490},
#     "Jolly Rancher Remix": {"x": 2210, "y": 1660},
#     "Mix'd Flavored By Jolly Rancher": {"x": 2560, "y": 1810},

#     "Wildcat's Revenge": {"x": 1900, "y": 2490},
#     "Wild Mouse": {"x": 1580, "y": 2290},
#     "Laff Trakk": {"x": 1370, "y": 2630},
#     "Lightning Racer": {"x": 1230, "y": 2140},

#     "Ferris Wheel": {"x": 3070, "y": 1560},
#     "Reese's Cupfusion": {"x": 3260, "y": 1810},
#     "Cocoa Cruiser": {"x": 2940, "y": 1730},
#     "Twizzlers Twisted Gravity": {"x": 3190, "y": 1340},
# }
