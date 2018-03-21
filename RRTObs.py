import numpy
import cv2
import random
import math

WINDOW = "RRT_Widnow"


DISPLAY = True
SHOWREWIRE = True
DISPINT = 100
MAXNODES = 5000

WHITE   = (255,255,255)
BLACK   = (0,0,0)
RED     = (0,0,255)
GREEN   = (0,255,0)
BLUE    = (255,0,0)
MAGENTA = (255,0,255)
YELLOW  = (0,255,255)
CYAN    = (255,255,0)



BGCOLOR   = BLACK
NODECOLOR = CYAN
LINECOLOR = CYAN
PATHCOLOR = RED

MAPHEIGHT = 2000
MAPWIDTH  = MAPHEIGHT

START = (500,500) 
END   = (MAPWIDTH-1,MAPHEIGHT-1)

TEXTLOC = (5+0,MAPHEIGHT-5)

LINESIZE = 2
NODESIZE = (LINESIZE + 1)

STEPSIZE = (MAPHEIGHT + MAPWIDTH)/2 * .1

def destroyImage(image):
    cv2.imshow(WINDOW, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def draw(image, nodes, pathed,redraw):
    
    cv2.circle(image, END, int(STEPSIZE), PATHCOLOR)

    if SHOWREWIRE:
        for place in redraw:
            cv2.line(image, place, redraw[place], WHITE, LINESIZE)
        cv2.imshow(WINDOW, image)
        cv2.waitKey(1)
    for place in redraw:
        cv2.line(image,place,redraw[place],BGCOLOR,LINESIZE)

    redraw.clear()   

    for place in nodes:

        cv2.circle(image,place, NODESIZE, NODECOLOR,-1)
        cv2.line(image,place,nodes[place],LINECOLOR,LINESIZE)

    if pathed == 1:
       pathedDraw(image,nodes)
        
    cv2.circle(image, START, NODESIZE+2, PATHCOLOR, -1)
    cv2.circle(image, END, NODESIZE+2, PATHCOLOR, -1)
    cv2.putText(image, "N: " + str(len(nodes)-DISPINT), TEXTLOC, 5, 1, BGCOLOR, 1)
    cv2.putText(image, "N: " + str(len(nodes)), TEXTLOC, 5, 1, RED, 1)

    cv2.imshow(WINDOW,image)
    cv2.waitKey(1)

def pathedDraw(image, nodes):
    #print("display path")
    node = END
    #counter = 0
    
    while node is not START:
        #counter +=1
        #print("counter" + str(counter))
        #print("node" + str(node))
        #print("parent" + str(nodes[node]))
       
        
        cv2.line(image,node,nodes[node],RED,LINESIZE)
        cv2.circle(image, node, NODESIZE, RED, -1)
        node = nodes[node]
        #if counter > 75:
            #cv2.imshow(WINDOW, image)
            #cv2.waitKey(0)
            #counter = "hello"
        #cv2.circle(image, node, NODESIZE+1, BGCOLOR, -1)


def euclDist(n1,n2):
    #returns euclidian distance
    return math.sqrt( ((n1[0] - n2[0])**2) + ((n1[1] - n2[1])**2) )
def distanceSortLambda(origin):
    '''
    returns a lambda to sort a function by distance from a point
    
    :param origin: the point to find distance from
    :return lambda: function that finds distance between origin and x
    ------stolen from James----------
    '''
    return lambda x: euclDist(origin, x)
def rewire(newNode,nodelist,costs,image):
    redraw = {}
    for node in nodelist:
        if node == newNode:
            continue
        if euclDist(node, newNode) > STEPSIZE:
            continue
        newCost = costs[newNode] + euclDist(node, newNode)
        if newCost < costs[node]:
            cv2.line(image, node, nodelist[node], BGCOLOR, LINESIZE)
            redraw[node]= nodelist[node]
            if node == nodelist[node]:
                print("5")
                return
            nodelist[node] = newNode
            if node == newNode:
                print("6")
                return
            costs[node] = newCost
    return redraw        

def finalPath(image, nodes):
    if END not in nodes:
        print("END NOT FOUND (try increasing MAXNODES)")
        return
    path = [END]
    place = nodes[END]
    while place is not START:
        print("place: " + str(place))
        path.append(place)
        place = nodes[place]
    path.append(place)
    path = path[::-1]


    for i in range(0,len(path)-1):
        current = path[i]
        next    = path[i+1]

        x,y   = current
        xf,yf   = next

        dx = xf-x
        dy = yf-y

        d = dx

        if d == dx:
            while x != xf:
                cv2.circle(image, (x,y), LINESIZE+5, MAGENTA, -1)
                cv2.imshow(WINDOW, image)
                cv2.waitKey(2)
                dx = xf-x
                dy = yf-y
                x+=1
                y+=int(dy/dx)
        '''elif d ==dy:
                                    while y != yf:
                                        cv2.circle(image, (x,y), LINESIZE+2, CYAN, -1)
                                        cv2.imshow(WINDOW, image)
                                        cv2.waitKey(2)
                                        y+=1
                                        x+=int(dx/dy)'''



    cv2.imshow(WINDOW, image)

def main():
    endFound = 0
    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    scale = 800/MAPHEIGHT
    cv2.resizeWindow(WINDOW, 800, 800)

    #make the map
    map = numpy.zeros((MAPWIDTH,MAPHEIGHT,3))
    map[:][:] = BGCOLOR

    nodelist = {START:START}
    costs = {}

    costs[START] = 0
    redraw = {}
    while len(nodelist) < MAXNODES:
        #if len(nodelist) % DISPINT == 0:
            #print(len(nodelist))
        newX = random.randint(0,MAPWIDTH)
        newY = random.randint(0,MAPHEIGHT)
        newNode = (newX,newY)

        #set default distance and parent, in case the start is the least dist
        parent = START

        neighbors = sorted( nodelist, key=distanceSortLambda(newNode))
        parent = neighbors[0]
        minCost = costs[parent] + euclDist(newNode, parent)

        for place in neighbors[0:4]:
            compCost = costs[place] + euclDist(newNode, place)
            if compCost < minCost:
                minCost = compCost
                parent = place
        dist = euclDist(newNode, parent)
        if nodelist.has_key(newNode):
            continue
        if newNode == END:
            continue
        if dist > STEPSIZE:
            continue

        #
        #
        #insert the check for collision
        #
        #

        costs[newNode] = minCost

        nodelist[newNode] = parent
        if newNode == parent:
            print("1")
            return
        redraw.update(rewire(newNode, nodelist, costs, map))


        if euclDist(newNode, END) < STEPSIZE:
            if endFound == 1:
                if euclDist(newNode, END) < euclDist(nodelist[END], END):
                    redraw[END] = nodelist[END]
                    if END == nodelist[END]:
                        print("2")
                        return
                    nodelist[END]=newNode
                    if END == newNode:
                        print("3")
                        return
                    costs[END]= costs[newNode] + euclDist(END, newNode)
                    endFound = 1
                    #print("FOUND THE END")
            else:
                nodelist[END]=newNode
                if END == newNode:
                    print("4")
                    return
                costs[END]= costs[newNode] + euclDist(END, newNode)
                endFound = 1

        

        #if the newly added node is close enough to the end, go for it!
        '''
        if euclDist(newNode, END) < STEPSIZE:
            dist = euclDist(newNode, END)
            for place in nodelist:
                testDist = euclDist(place, END)
                if testDist > dist:
                    nodelist[END]=newNode
        '''
        
        if len(nodelist) % DISPINT == 0 and DISPLAY:
            draw(map,nodelist,endFound,redraw)
    draw(map, nodelist, endFound, redraw)
    #finalPath(map,nodelist)
    destroyImage(map)


if __name__ == '__main__':
    main()
