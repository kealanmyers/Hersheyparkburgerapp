import math

#create dicr of all hershey rides, noting ride type and grid cords
#overlay a grid onto hershey park map to assign all rides an x and y value for cords
rides = {
    "Candymonium": {"x": 4040, "y": 2210},
    "Carrousel": {"x": 3830, "y": 2390},

    "Skyrush": {"x": 3660, "y": 1430},
    "Comet": {"x": 3380, "y": 1570},
    "SooperDooperLooper": {"x": 3820, "y": 1260},

    "Kissing Tower": {"x": 3190, "y": 760},
    "Great Bear": {"x": 3310, "y": 950},
    "Coal Cracker": {"x": 3460, "y": 820},

    "Trailblazer": {"x": 2780, "y": 1480},
    "Storm Runner": {"x": 2420, "y": 1490},
    "Jolly Rancher Remix": {"x": 2210, "y": 1660},
    "Mix'd Flavored By Jolly Rancher": {"x": 2560, "y": 1810},

    "Wildcat's Revenge": {"x": 1900, "y": 2490},
    "Wild Mouse": {"x": 1580, "y": 2290},
    "Laff Trakk": {"x": 1370, "y": 2630},
    "Lightning Racer": {"x": 1230, "y": 2140},

    "Ferris Wheel": {"x": 3070, "y": 1560},
    "Reese's Cupfusion": {"x": 3260, "y": 1810},
    "Cocoa Cruiser": {"x": 2940, "y": 1730},
    "Twizzlers Twisted Gravity": {"x": 3190, "y": 1340},
}

def main():
    #determine user's location
    location = str(input("What ride are you at? ").strip())
    location = location.title()
    #determine the closest rides to user
    getclose(location)

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
    ridedistance = {
    "Candymonium": {getdistance(x, y, 4040, 2210)},
    "Carrousel": {getdistance(x, y, 3830, 2390)},

    "Skyrush": {getdistance(x, y, 3660, 1430)},
    "Comet": {getdistance(x, y, 3380, 1570)},
    "SooperDooperLooper": {getdistance(x, y, 3820, 1260)},

    "Kissing Tower": {getdistance(x, y, 3190, 760)},
    "Great Bear": {getdistance(x, y, 3310, 950)},
    "Coal Cracker": {getdistance(x, y, 3460, 820)},

    "Trailblazer": {getdistance(x, y, 2780, 1480)},
    "Storm Runner": {getdistance(x, y, 2420, 1490)},
    "Jolly Rancher Remix": {getdistance(x, y, 2210, 1660)},
    "Mix'd Flavored By Jolly Rancher": {getdistance(x, y, 2560, 1810)},

    "Wildcat's Revenge": {getdistance(x, y, 1900, 2490)},
    "Wild Mouse": {getdistance(x, y, 1580, 2290)},
    "Laff Trakk": {getdistance(x, y, 1370, 2630)},
    "Lightning Racer": {getdistance(x, y, 1230, 2140)},

    "Ferris Wheel": {getdistance(x, y, 3070, 1560)},
    "Reese's Cupfusion": {getdistance(x, y, 3260, 1810)},
    "Cocoa Cruiser": {getdistance(x, y, 2940, 1730)},
    "Twizzlers Twisted Gravity": {getdistance(x, y, 3190, 1340)},
}
    #sorts ridedistance from shortest to longerst distance
    sorteddistance = dict(sorted(ridedistance.items(), key=lambda item: item[1]))

    #gathers the shortest 6 distances, excluding the current ride, returns them
    closesix = [

    ]
    for i in sorteddistance:
        if len(closesix) < 6:

    

def square(n):
    return(n * n)

def getdistance(x1, y1, x2, y2):
    return(math.sqrt((square(x1 - x2)) + (square(y1 - y2))))


def getwait():
    #access online wait time information from hershey website for specific rides
    pass


getclose("Candymonium")