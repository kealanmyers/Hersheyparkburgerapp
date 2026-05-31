import requests as r
url = "https://queue-times.com/parks/15/queue_times.json"
response = r.get(url)
data = response.json()

ridelookup = {

}

for land in data["lands"]:
    for ride in land["rides"]:
        ridelookup[ride["name"].strip().lower()] = ride

print(ridelookup["skyrush"])
    