import requests as r

from data import QUEUE_TIMES_URL

response = r.get(QUEUE_TIMES_URL)
data = response.json()
print(data)