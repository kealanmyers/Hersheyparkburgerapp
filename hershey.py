import math

from data import rides


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
                if getdistance(x, y, x2, y2):
                    pass

    #determine which rides of the chosen type are closest by comparing grid cordinates
    #list 6 closest rides
    pass

def square(n):
    return(n * n)

def getdistance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def getwait():
    #access online wait time information from hershey website for specific rides
    pass

if __name__ == "__main__":
    main()