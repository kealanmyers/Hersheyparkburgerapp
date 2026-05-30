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

    "Whitecap Racer": {"x": 1790, "y": 1650},
    "Breakers Edge": {"x": 1960, "y": 1570},
    "Intercoastal Waterway": {"x": 1650, "y": 1830},

    "Ferris Wheel": {"x": 3070, "y": 1560},
    "Reese's Cupfusion": {"x": 3260, "y": 1810},
    "Cocoa Cruiser": {"x": 2940, "y": 1730},
    "Twizzlers Twisted Gravity": {"x": 3190, "y": 1340},
}
def main():
    #determine user's location
    location = str(input("What ride are you at? ").strip())
    location = location.title()
    getclose(location)

#ask user for ride they are closest to at hershey park
#sort obtained type of ride by distance, closest to farthest
#print wait time along with name of ride in order of closest to furthest

def getcords(location):
    x = rides[location]["x"]
    y = rides[location]["y"]
    return(x, y)

def getclose(location):
    x, y = getcords(location)

    ########burger please fix###########
    closestrides = []
    for i in rides:
        if len(closestrides) < 6:
            closestrides.add(i)
        else:
            for j in closestrides:
                x2, y2 = getcords(j)
                if getdistance(x, y, x2, y2)

    #determine which rides of the chosen type are closest by comparing grid cordinates
    #list 6 closest rides
    pass

def square(n):
    return(n * n)

def getdistance(x1, y1, x2, y2):
    return(math.sqrt((square(x1 - x2)) + (square(y1 - y2))))


def getwait():
    #access online wait time information from hershey website for specific rides
    pass
main()