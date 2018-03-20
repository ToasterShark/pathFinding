import numpy
import cv2
import random
import math

WINDOW = "RRT_Widnow"

BGCOLOR   = (255,255,255)
NODECOLOR = (0,0,0)
LINECOLOR = (0,0,0)
PATHCOLOR = (255,0,0)

MAPHEIGHT = 1000
MAPWIDTH  = 1000

START = (100,100)
END   = (900,900)

MAXNODES = 1000

LINESIZE = 2
NODESIZE = 4

EPSILON = (MAPHEIGHT + MAPWIDTH)/2 * .1

endFound = 0

def draw(image, nodes):

    for place in nodes:

        cv2.circle(image,place, NODESIZE, NODECOLOR)
        cv2.line(image,place,nodes[place],LINECOLOR,LINESIZE)

    if endFound == 1:
        node = END
        while node != START:
            cv2.line(image,node,nodes[node],PATHCOLOR,LINESIZE)
            node = nodes[node]

    cv2.imshow(WINDOW,image)
    cv2.waitKey(1)

def euclDist(n1,n2):
    #returns euclidian distance
    return math.sqrt( ((n1[0] - n2[0])**2) + ((n1[1] - n2[1])**2) )

def main():
  cv2.namedWindow(WINDOW, cv2.WINDOW_AUTOSIZE)

  #make the map
  map = numpy.zeros((MAPWIDTH,MAPHEIGHT,3))
  map[:][:] = BGCOLOR

  nodelist = {START:START}

  draw(map,nodelist)

  while len(nodelist) < MAXNODES:
    newX = random.randint(0,MAPWIDTH)
    newY = random.randint(0,MAPHEIGHT)
    newNode = (newX,newY)

    #set default distance and parent, in case the start is the least dist
    dist = euclDist(START,newNode)
    parent = START

    for place in nodelist:
        testDist = euclDist(newNode,place)
        if testDist < dist:
            dist    = testDist
            parent  = place

    if dist > EPSILON:
        continue

    if newNode == END:
        endFound = 1
    nodelist[newNode] = parent

    draw(map,nodelist)

if __name__ == '__main__':
    main()
