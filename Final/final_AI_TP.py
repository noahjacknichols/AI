import string
import math
import sys
from queue import PriorityQueue

def main():
    fileName = str(sys.argv[1])
    if(fileName[-3:] != 'txt'):
        print("please input a text like so. 'python AI_TP.py <textfile.txt>")
        return 0
    try:
            
        rL,rW,numRobots,robotArray,rend,room = getInput(fileName)
        i = 0
        pathArray = []
        complete = False
        robotNum = 0
        for robot in robotArray:
            print("finding initial robot",robotNum,"path..")
            path = Astar(room,robot,rend,rL,rW)
            tracePath = traceStack(path, rend)
            # print("path for robot{}:{}".format(robot, tracePath))
            pathArray.append(tracePath)
            robotNum+=1

        k = 0

        
        while(complete != True):
            print("checking collision..")
            for i in range(len(pathArray)):
                for j in range(len(pathArray)):
                    # print(i,j)
                    if(i!= j and type(pathArray[i]) is not str and type(pathArray[j]) is not str):
                        overlap = min(len(pathArray[i]), len(pathArray[j]))
                        for k in range(overlap):
                            # print("1st arr:",pathArray[i])
                            # print("2nd arr:", pathArray[j])
                            if(pathArray[i][k] == pathArray[j][k]):
                                # print("same values, run again")
                                room = editRoom(pathArray[j][k], room, 1)

                                pathArray[j] = traceStack(Astar(room, robotArray[j], rend, rL, rW), rend)
                                # print("new path:",pathArray[j])
                                room = editRoom(pathArray[j][k], room, 0)


            flag = 0
            for i in range(len(pathArray)):
                for j in range(len(pathArray)):
                    if(i!= j and type(pathArray[i]) is not str and type(pathArray[j]) is not str):
                        overlap = min(len(pathArray[i]), len(pathArray[j]))
                        for k in range(overlap):
                            if(pathArray[i][k] == pathArray[j][k]):
                                #same value, run again
                                flag = 1
            if(flag == 0):
                complete = True
            

                    
                                

            # printRoom(room, rL, rW)
        # print("paths:")
        # print(pathArray)
        i = 0
        for path in pathArray:
            print("path for robot",i,":{}".format(path))
            if(type(path) is not str):
                room = updateRoom(path, room, i)
            i+=1
        
        addPoints(room, robotArray, rend)
        printRoom(room, rL, rW)
        # writeRoom(room)
        print()
        print("finished.")
    except:
        print("something seems to be wrong with the given file. Please check for errors and try again.")
#-----------------------------------------------------------
# Parameters:   room (list), start (tuple), goal (tuple), rl (int), rw (int)
#               
# Return:       previous (dict)
# Description:  finds the path for the given start node to rendezvous
#-----------------------------------------------------------
def Astar(room,start, goal, rL, rW):
    frontier = PriorityQueue()
    frontier.put((0,start))
    previous = {}
    current_cost = {}
    previous[start] = None
    current_cost[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal:

            break
        neighbors = getNeighbors(current[1],rL-1,rW-1, room)

        for element in neighbors:
            new_cost = current_cost[current[1]] + cost(start,element)

            if element not in current_cost or new_cost< current_cost[element]:
                current_cost[element] = new_cost
                priority = new_cost + cost(goal,element)
                frontier.put((priority, element))
                previous[element] = current[1]
    return previous

def editRoom(location, room, val):
    # print(location)
    room[location[1]][location[0]] = str(val)
    return room

# def writeRoom(room):
    # f = open("output.txt", 'w')
    # for i in room:
    #     row = ""
    #     for j in i:
    #         row = row +(j)
    #     f.write(row)
        
    # f.close()
#-----------------------------------------------------------
# Parameters:   previous (dict), room(list), i (int)
#               
# Return:       room(list)
# Description:  updates the room with the last robots path
#-----------------------------------------------------------
def updateRoom(previous, room, i):
    x = 'A'
    for node in previous:
        if(room[node[1]][node[0]] == "{}".format(chr(ord(x)))):
            room[node[1]][node[0]] = 'I'
        room[node[1]][node[0]] = "{}".format(chr(ord(x)+i))
    return room

#-----------------------------------------------------------
# Parameters:   room (list), robotArray (list of tuples), rend (tuple)
#               
# Return:       None
# Description:  updates the room with the robots starting points, and Rendezvous point
#-----------------------------------------------------------

def addPoints(room, robotArray,rend):
    x = 'A'
    i = 0
    for robot in robotArray:
        # print("robot pos:", robot[0],robot[1])
        room[robot[1]][robot[0]] = "{}".format(chr(ord(x)+i))
        i+=1
    # print("rend pos:",rend[0],rend[1])
    room[rend[1]][rend[0]] = "R"

#-----------------------------------------------------------
# Parameters:   previous (dict)
#               
# Return:       l (list)
# Description:  returns the list of tuples that the robot took in correct order
#-----------------------------------------------------------

def traceStack(previous, goal):
    curNode = goal
    if(goal not in previous):
        return 'could not get to rendezvous'
    l = []
    l.append(curNode)
    while(previous[curNode] != None):
        curNode = previous[curNode]
        if(curNode != None):
            l.insert(0,curNode)
    return l

#-----------------------------------------------------------
# Parameters:   current (tuple), nextNode(tuple)
#               
# Return:       final_cost (float)
# Description:  finds the cost to move from current node to next node
#-----------------------------------------------------------

def cost(current, nextNode):
    final_cost = abs(current[0] - nextNode[0]) + abs(current[1] - nextNode[1])
    return float(final_cost)

#-----------------------------------------------------------
# Parameters:   current (tuple), rl(int), rw(int), room(list)
#               
# Return:       neighbors(list)
# Description:  returns the list of nieghbors that are legal-moves
#-----------------------------------------------------------
def getNeighbors(current, rL, rW, room):
    neighbors = []
    # print(current[1],current[0])
    # print("I AM HERE")
    # print(room)
    # print("room at pos:",room[current[1]])
    if current[0] > 0:
        if(room[current[1]][current[0]-1]) != '1':
            neighbors.append((current[0]-1,current[1]))
    if current[1] > 0:
        if(room[current[1]-1][current[0]]) != '1':
            neighbors.append((current[0],current[1]-1))
    if current[1] < rL:
        if(room[current[1]+1][current[0]]) != '1':
            neighbors.append((current[0],current[1]+1))
    if current[0] < rW:
        if(room[current[1]][current[0]+1]) != '1':
            neighbors.append((current[0]+1,current[1]))

    return neighbors
    
#-----------------------------------------------------------
# Parameters:   room(list), rl(int), rw(int)
#               
# Return:       None
# Description:  prints the room
#-----------------------------------------------------------
def printRoom(room,rL,rW):
    for i in range(rL-1,-1,-1):
        print()
        for j in range(rW):
            print(room[i][j],end='')
    print()

#-----------------------------------------------------------
# Parameters:   filename(string)
#               
# Return:       rl(int), rw(int), numRobots(int), robotArray(list),rend (tuple),room(list)
# Description:  returns all of the variables in the given text file named filename
#-----------------------------------------------------------
def getInput(filename):
    with open(filename) as fp:
        line = fp.readline()
        words = line.split()
        rL = int(words[0])
        rW = int(words[1])
        # print("rl,rw:",rL,rW)
        room = []
        line=fp.readline()
        words = line.split()
        numRobots = int(words[0])

        robotArray = []
        for i in range(numRobots):
            line = fp.readline()
            words = line.split()
            robotArray.append((int(words[0]),int(words[1])))
        line = fp.readline()
        words=line.split()

        lines = fp.readlines()

        rend = ((int(words[0]),int(words[1])))
        # print(rend)
        #lines = lines[1:]
        #print(lines)
        count2 = 0
        for line in lines:

            count = 0
            line = line.strip()
            # print(line)
            #for j in range(len(line)):
            row = []
            for element in line:
                #print(count)
                row.append(str(element))
                # print(element)
                count+=1
            count2+=1
            # print(row)
            room.append(row)
            # print(room)
            # print(count2,count)
        # print(room)
    newRoom = []
    for row in room:
        newRoom.insert(0,row)
    # print("ROOM IS NOW:",room)
    return rL,rW,numRobots,robotArray,rend,newRoom


if __name__ == '__main__':

    main()