import numpy
import cv2
import random
import math

WINDOW          = "RRT_Widnow"


MAZEBOOL        = True

DISPLAY         = True
SHOWREWIRE      = True
DISPINT         = 1
MAXNODES        = 10000


WHITE           = (255,255,255)
BLACK           = (0,0,0)
RED             = (0,0,255)
GREEN           = (0,255,0)
BLUE            = (255,0,0)
MAGENTA         = (255,0,255)
YELLOW          = (0,255,255)
CYAN            = (255,255,0)



BGCOLOR         = BLACK
NODECOLOR       = CYAN
LINECOLOR       = CYAN
PATHCOLOR       = RED

MAPHEIGHT       = 1000
MAPWIDTH        = MAPHEIGHT

START           = (1,1) 
END             = (MAPWIDTH-1,MAPHEIGHT-1)

TEXTLOC         = (5+0,MAPHEIGHT-5)

LINESIZE        = 2
NODESIZE        = (LINESIZE + 1)

STEPSIZE        = (MAPHEIGHT + MAPWIDTH)/2 * .1

ix,iy   = -1,-1
drawing = False
mode    = True


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
        
    cv2.circle(image, START, NODESIZE+4, YELLOW, -1)
    cv2.circle(image, END, NODESIZE+2, PATHCOLOR, -1)
    cv2.putText(image, "N: " + str(len(nodes)-DISPINT), TEXTLOC, 5, 2, BGCOLOR, 1)
    cv2.putText(image, "N: " + str(len(nodes)), TEXTLOC, 5, 2, RED, 1)

    cv2.imshow(WINDOW,image)
    cv2.waitKey(1)

def pathedDraw(image, nodes):
    #print("display path")
    node = END
    counter = 0
    print("before while START: " + str(START))
    while (node[0] != START[0]) and (node[1] != START[1]):
        counter +=1
        print("counter" + str(counter))
        print("node" + str(node))
        print("parent" + str(nodes[node]))
       
        
        cv2.line(image,node,nodes[node],PATHCOLOR,LINESIZE)
        cv2.circle(image, node, NODESIZE, PATHCOLOR, -1)
        node = nodes[node]
        if counter > 75:
            cv2.imshow(WINDOW, image)
            cv2.waitKey(0)
            counter = "hello"
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
    global oblist
    redraw = {}
    for node in nodelist:
        if node == newNode: continue

        if euclDist(node, newNode) > STEPSIZE: continue
        if collide(node,newNode,oblist): continue
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
    return redraw,nodelist,costs

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

def drawObstacles(event,x,y,flags,param):
    global ix,iy,drawing,mode,oblist

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode:
            cv2.line(img,(ix,iy),(x,y),MAGENTA,LINESIZE)
            oblist.append(((ix,iy),(x,y)))
        else:
            cv2.circle(img,(ix,iy),int(euclDist((ix,iy),(x,y))),MAGENTA,-1)

img = numpy.zeros((MAPWIDTH,MAPHEIGHT,3))
oblist = []

def ccw(A,B,C):
    first  = (C[1] - A[1]) * (B[0] - A[0])
    second = (B[1] - A[1]) * (C[0] - A[0])
    return first > second

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def collide(node,newNode,oblist):
    rtn = False
    for seg in oblist:
        if intersect(node,newNode,seg[0],seg[1]):
            rtn = True
            break
    return rtn

def move(nodes,costs):#only call this method once the path has been found
    global START
    node = END
    falsestart = START
    while nodes[node] is not START:
        print(nodes[node])
        node = nodes[node]
    #node should be equal to the node after START on the path
    START = node
    nodes[START] = START
    nodes[falsestart] = START
    costs[START] = 0

    neighbors = sorted( nodes, key=distanceSortLambda(START))
    for i in range(0,len(neighbors)):
        cost = 0
        n = neighbors[i]
        while nodes[n][0] != START[0] and nodes[n][1] != START[1]:
            cost += euclDist(n,nodes[n])
            n = nodes[n]

        costs[neighbors[i]] = cost
    cv2.waitKey(1000)

    return nodes,costs
    #if im not mistaken, using global to call START should allow me to overwrite the global value for START

    #then rewire according to the new start value (outside of this method)


def main():
    endFound = 0
    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    scale = 800/MAPHEIGHT
    cv2.resizeWindow(WINDOW, 800, 800)

    #make mousecallback
    cv2.setMouseCallback(WINDOW,drawObstacles)

    #make the map
    global img,mode
    img[:][:] = BGCOLOR

    nodelist = {START:START}
    costs = {}

    costs[START] = 0
    redraw = {}

    arrived = 0
    #array of tuples in form ((p1x,p1y),(p2x,p2y))
    

    #draw obstacles
    
    print("draw your obstacles, press q to end")
    while True:
        cv2.imshow(WINDOW,img)
        k = cv2.waitKey(10) & 0xFF
        if k == ord("m"): mode = not mode
        elif k == ord("q"): break

    while len(nodelist) < MAXNODES and arrived != 1:
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
            dx = newNode[0]-parent[0]
            dy = newNode[1]-parent[1]

            dx = int(dx*STEPSIZE/dist)
            dy = int(dy*STEPSIZE/dist)

            newNode = (parent[0]+dx), (parent[1]+dy)
        if collide(parent,newNode,oblist):
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
        rewired,nodelist,costs = rewire(newNode,nodelist,costs,img)
        redraw.update(rewired)


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
            draw(img,nodelist,endFound,redraw)
            if END is START:
                print("arrived")
                arrived = 1
            elif endFound == 1:
                global DISPINT
                DISPINT = 1
                print("before move")
                
                nodelist,costs = move(nodelist,costs)
                print("after move")

                neighbors = sorted( nodelist, key=distanceSortLambda(START))
                for i in range(0,len(neighbors)):
                    rewired,nodelist,costs = rewire(nodelist[parent],nodelist,costs,img)
                    redraw.update(rewired)
                #n = END
                #while n is not START:
                #    rewired,nodelist,costs = rewire(n,nodelist,costs,img)
                #    redraw.update(rewired)
                #    n = nodelist[n]
                draw(img,nodelist,endFound,redraw)
    draw(img, nodelist, endFound, redraw)
    #finalPath(img,nodelist)
    destroyImage(img)


if __name__ == '__main__':
    main()
