"""
All Hersheypark constants live here.

- Edit the RIDES list to add or change rides.
- List order = API index (first ride is 0, second is 1, etc.)
"""

QUEUE_TIMES_URL = "https://queue-times.com/parks/15/queue_times.json"

# (name, x, y) on the park map grid
RIDES = [
    {"name": "Breakers Edge", "x": 1960, "y": 1570},
    {"name": "Candymonium", "x": 4040, "y": 2210},
    {"name": "Carrousel", "x": 3830, "y": 2390},
    {"name": "Coal Cracker", "x": 3460, "y": 820},
    {"name": "Cocoa Cruiser", "x": 2940, "y": 1730},
    {"name": "Comet", "x": 3380, "y": 1570},
    {"name": "Ferris Wheel", "x": 3070, "y": 1560},
    {"name": "Great Bear", "x": 3310, "y": 950},
    {"name": "Intercoastal Waterway", "x": 1650, "y": 1830},
    {"name": "Jolly Rancher Remix", "x": 2210, "y": 1660},
    {"name": "Kissing Tower", "x": 3190, "y": 760},
    {"name": "Laff Trakk", "x": 1370, "y": 2630},
    {"name": "Lightning Racer", "x": 1230, "y": 2140},
    {"name": "Mix'd Flavored By Jolly Rancher", "x": 2560, "y": 1810},
    {"name": "Reese's Cupfusion", "x": 3260, "y": 1810},
    {"name": "Skyrush", "x": 3660, "y": 1430},
    {"name": "SooperDooperLooper", "x": 3820, "y": 1260},
    {"name": "Storm Runner", "x": 2420, "y": 1490},
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
