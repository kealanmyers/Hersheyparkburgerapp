import requests as r

from data import QUEUE_TIMES_URL

response = r.get(QUEUE_TIMES_URL)
data = response.json()

ridelookup = {

}

for land in data["lands"]:
    for ride in land["rides"]:
        ridelookup[ride["name"].strip().lower()] = ride

print(ridelookup["skyrush"])
    