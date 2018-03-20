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
END   = (MAPHEIGHT-100,MAPWIDTH-100)

MAXNODES = 3000

LINESIZE = (MAPHEIGHT+MAPWIDTH)/1000
NODESIZE = (LINESIZE + 1)

STEPSIZE = (MAPHEIGHT + MAPWIDTH)/2 * .2

def destroyImage(image):
    cv2.imshow(WINDOW, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def draw(image, nodes, pathed):
    
    cv2.circle(image, END, int(STEPSIZE), PATHCOLOR)


    for place in nodes:

        cv2.circle(image,place, NODESIZE, NODECOLOR,-1)
        cv2.line(image,place,nodes[place],LINECOLOR,LINESIZE)

    #if pathed == 1:
    #   pathedDraw(image,nodes)
        
    cv2.circle(image, START, NODESIZE+2, PATHCOLOR, -1)
    cv2.circle(image, END, NODESIZE+2, PATHCOLOR, -1)

    cv2.imshow(WINDOW,image)
    cv2.waitKey(1)

def pathedDraw(image, nodes):
    #print("display path")
    node = END
    while node != (100,100):
        print("node" + str(node))
        print("parent" + str(nodes[node]))
        cv2.line(image,node,nodes[node],PATHCOLOR,LINESIZE+1)
        node = nodes[node]


def euclDist(n1,n2):
    #returns euclidian distance
    return math.sqrt( ((n1[0] - n2[0])**2) + ((n1[1] - n2[1])**2) )

def main():
    endFound = 0
    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    scale = 800/MAPHEIGHT
    cv2.resizeWindow(WINDOW, 800, 800)

    #make the map
    map = numpy.zeros((MAPWIDTH,MAPHEIGHT,3))
    map[:][:] = BGCOLOR

    nodelist = {START:START}

    draw(map,nodelist,endFound)

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
        if newNode == END:
            continue
        if dist > STEPSIZE:
            continue
        if euclDist(newNode, END) < STEPSIZE:
            nodelist[END]=newNode
            endFound = 1
            #print("FOUND THE END")
        nodelist[newNode] = parent
        #if the newly added node is close enough to the end, go for it!
        if euclDist(newNode, END) < STEPSIZE:
            dist = euclDist(newNode, END)
            for place in nodelist:
                testDist = euclDist(place, END)
                if testDist > dist:
                    nodelist[END]=newNode

        if len(nodelist) % 1 == 0:
            draw(map,nodelist,endFound)
    destroyImage(map)


if __name__ == '__main__':
    main()
