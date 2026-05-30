import requests as r
url = "https://queue-times.com/parks/15/queue_times.json"
response = r.get(url)
data = response.json()
print(data)