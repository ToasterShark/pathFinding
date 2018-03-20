import numpy
import cv2
import Queue
import math

imagename  = "maze3.png"

def main():
    map = cv2.imread(imagename, 1)
    editable = numpy.copy(map)
    cv2.namedWindow("a*", cv2.WINDOW_NORMAL,)

    #coordinates in (x,y) format
    begin = (50,50)
    end = (99,99)
    print("\n before aStar begins")
    path = aStar(begin,end,map,255,editable)

    for step in path:
        print(step)
        editable[step[0]][step[1]] = (0,0,255)

    cv2.imshow("a*", editable)
    cv2.waitKey(0)

def aStar(start,finish,map,space,newmap):
    point,parents,cost = pathing(start,finish,map,space,newmap)
    if cost == -1:
        return [(0,0), start]
    else:
        path = []
        trace = point
        while trace != None:
            path.append(trace)
            trace = parents[trace]
        return path

def pathing(s,f,m,space,nm):
    cv2.namedWindow("a*", cv2.WINDOW_NORMAL)
    #list of unexplored points
    #priority queue makes points closer to goal first
    unexplored = Queue.PriorityQueue()
    unexplored.put((0,s))

    #list of parents so u know the path once ur finished
    parents = {}
    parents[s] = None #start has no parents.. so

    #list of costs to the location
    costs = {}
    costs[s] = 0 #u start at start so u dont have to get there

    #lets explore the unexplored
    counter = 0
    while not unexplored.empty():
        #point is the current point
        point = unexplored.get()[1]
        
        if counter % 50 == 0:
            cv2.imshow("a*",nm)
            cv2.waitKey(10)
        if point == f:
            #ur here bud! congrats
            return point,parents,costs[point]
        if(point[0] >= len(m) or point[0] < 0 or point[1] >= len(m[0]) or point[1] < 0):
            #out of bounds
            continue
        if numpy.all(m[point[0]][point[1]] != space):
            #ur in a wall, how did u do this
            continue
        #check the possible next steps
        nm[point[0]][point[1]]=(0,255,0)
        for step in surrounding(point):
            cost = costs[point] + dist(point,step)
            #check for new lowest cost
            if not step in costs or cost < costs[step]:
                costs[step] = cost
                stepworth = .1*cost + goal(step,f)

                #puts new step in the unexplored list
                unexplored.put((stepworth,step))
                parents[step] = point
        counter+=1

    return s,parents,-1


def surrounding(coord):
    x,y = coord
    rtn = [(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y),(x,y),(x+1,y),(x-1,y+1),(x,y+1),(x+1,y+1)]
    return rtn

def dist(point,neighbor):
    if(point[0] == neighbor[0] or point[1] == neighbor[1]):
        return 1
    else:
        return math.sqrt(2)

def goal(finish,point):
    dx = finish[0] - point[0]
    dy = finish[1] - point[1]
    euclidianDist = math.sqrt(dx**2 + dy**2)
    return euclidianDist

if __name__ == "__main__":
    main()