import math
import requests as r
from operator import itemgetter
from data import rides

#create dict of all hershey rides, noting grid cords
#assign all rides an x and y value for cords

def main():
    #determine user's location
    location = str(input("What ride are you at? ").strip().lower())
    location = location.title()
    #determine the closest rides to user
    sixnames = getclose(location)
    getwait(sixnames)
    
#sort obtained type of ride by distance, closest to farthest
#print wait time along with name of ride in order of closest to furthest

def getcords(location):
    x = rides[location]["x"]
    y = rides[location]["y"]
    return(x, y)

def getclose(location):
    #retrieves x and y cords for current ride
    x, y = getcords(location)
    #creates a dict with the distance from current ride to every other ride

    ridedistance = {}
    for i in rides:
        ridename = i
        distance = round(getdistance(x, y, rides[ridename]["x"], rides[ridename]["y"]))
        ridedistance[ridename] = distance


    #sorts ridedistance from shortest to longerst distance
    sorteddistance = dict(sorted(ridedistance.items(), key=itemgetter(1)))
    
    #gathers the shortest 6 distances, excluding the current ride, returns them
    closesixnames = []
    for i in sorteddistance:
         if i == location:
             pass
         elif len(closesixnames) < 6:
             closesixnames.append(i)

    return(closesixnames)

    
def square(n):
    return(n * n)

def getdistance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def getwait(sixnames):
    url = "https://queue-times.com/parks/15/queue_times.json"
    response = r.get(url)
    data = response.json()

    ridelookup = {}

    for land in data["lands"]:
        for ride in land["rides"]:
            ridelookup[ride["name"].strip().lower()] = ride

    for ridename in sixnames:
        key = ridename.lower()
        #if ride['is_open']:
            #print(f"{ridename}: {ridelookup[key]['wait_time']} min wait")
        #else:
            #print(f"{ridename}: Ride is closed")
        print(f"{ridename}: {ridelookup[key]['wait_time']} min wait")
        



main()
