
import sys
import queue

fullDomain = [1,2,3,4,5,6,7,8,9]


xPos = ['A','B','C','D','E','F','G','H','I']
yPos = ['1','2','3','4','5','6','7','8','9']


class cell:
    def init(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value

class CSP:
    def __init__(self, inp):
        self.inp = inp
        self.variables = [r + c for r in 'ABCDEFGHI' for c in '123456789']
        self.values = {}
        index = 0
        for x in self.variables:
            if(inp[index] == '0'):
                self.values[x] = [1,2,3,4,5,6,7,8,9]
            else:
                self.values[x] = int(inp[index])
            index+=1
        print(self.values)
        self.arcs = {}
        index = 0
        for x in range(0,9):
            for y in range(0,9):
                self.arcs[self.variables[index]] = self.setArcs(x,y)
                index += 1
        print("ARCS:")
        print(self.arcs)
        

    def printSudoku(self):
        dash = "+++++++++++++"
        line = ""
        counter = 0
        for y in range(0,9):
            if(y % 3  == 0):
                print(dash)
            for x in range(0,9):
                if(x%3 == 0):
                    line+='+'
                line+= self.inp[counter]
                counter+=1

            print(line+'+')
            line = ''
        print(dash)
        
    def setArcs(self, x,y):
        #find all constraints for x,y on board

        #horizontal constraints
        arcs = []
        for i in range(0,9):
            if(i!= x):
                arcs.append(xPos[i]+yPos[y])
        #vertical constraints
        for j in range(0,9):
            if(j!= y):
                arcs.append(xPos[x]+yPos[j])

        #subdomain constraints

        xDom = x - x % 3
        yDom = y - y % 3
        for i in range(0,3):
            for j in range(0,3):
                if(x!= j and y != i):
                    # print("X:",xDom+i, "Y:", yDom+j)
                    # print("ypos:",)
                    if(xPos[xDom+j]+yPos[yDom+i] not in arcs and (xPos[xDom+j]+yPos[yDom+i] != xPos[xDom+j]+yPos[yDom+i])):
                        arcs.append(xPos[xDom+j]+yPos[yDom+i])

        return arcs

    def getValues(self):
        return self.values

    def getVariables(self):
        return self.variables

    def getArcs(self):
        return self.arcs

    def getDomain(self, Xi):
        return self.values[Xi]
    def removeFromDomain(self, Xi, i):
        self.values[Xi].remove(i)

        # print("values:")
        
        # self.domain = [(var, fullDomain if self.values[self.variables.index(var)] == 0 else self.values[self.variables.index(var)]) for var in self.variables]
        # a = [self.colNeighbors(self.domain, i) for i in range(9)]
        # b = [self.rowNeighbors(self.domain, i) for i in range(9)]
        # c = [self.cellNeighbors(self.domain, i, j) for i in range(9) for j in range(9)]
        # self.allNeighbors = (a + b + c)

        # self.keys = dict((s, [u for u in self.allNeighbors if s in u]) for s in self.variables)
        # print(self.domain)
        # self.neighbors = dict((s, set(sum(self.keys[s], [])) - set([s])) for s in self.variables)
        # self.constraints = dict((variable, neighbor) for variable in self.variables for neighbor in self.neighbors[variable])
    
        # print(self.constraints)
        

    def colNeighbors(self, b, col):
        neighbors = []
        for i in range(col, len(b), 9):
            neighbors.append(b[i])

        return neighbors

    def rowNeighbors(self, b, row):
        neighbors = []
        end = (row + 1) * 9
        start = end - 9
        for i in range(start, end, 1):
            neighbors.append(b[i])

        return neighbors
    def cellNeighbors(self, b, row, col):
        # print("R:", row, "C:", col)
        neighbors = []
        domRow = row - row % 3
        domCol = col - col % 3
        for j in range(3):
            for i in range(3):
                    neighbors.append(b[(j+domCol) + (i+domRow)*9])
        return neighbors


#revision algorithm. reduces domain of Xi based on constraints
def revision(csp, Xi, Xj):
    i = 0
    domXi = csp.getDomain(Xi) #get domain of Xi eg. 'A1'
    domXj = csp.getDomain(Xj)
    isRevised = False
    for x in domXi:
        valid = True
        
        for y in domXj:
            if x != y:
                valid = False
        if valid:
            csp.removeFromDomain(Xi, i)
            isRevised = True
        else:
            i += 1
    return isRevised

class BTS():
    def __init__(self, csp):
        self.csp = csp
        self.unassigned = {}
        
        for key in self.csp.values.keys():
            values = self.csp.values[key]
            self.unnasigned[key] = True if len(values) != 1 else False
        
        return


    def unassignedValues(self):
        minKey = None
        minValues = None
        for key in self.unassigned.keys():
            values = self.csp.values[key]
            if minValues == None or len(values) < len(minValues):
                minKey = key
                minValues = values

        return (minKey, minValues)


    #input:
#   Xk(String) -->
    def testConsistency(self, key, value):
        result = True
        for Xk in self.csp.arcs[key]:
            values = self.csp.values[Xk]
            if(len(values) == 1 and values[0] == value):
                result = False
        return result

    def forwardCheck(self, key, value):
        return




def AC3_A_BITCH(csp):
    q = queue.Queue()
    arcs = csp.getArcs()
    variables = csp.getVariables()

    print("HERE:")
    # print(arcs)
    for var in variables:
        a = arcs[var]
        for arc in a:
            # print((var,arc))
            q.put((var,arc))
    print("finished")
    
    #GET ARCS -  call the function boi
    #GET NEIGHBORS - call function
    while not q.empty():
        (Xi, Xj) = q.pop()
        if(revision(csp,Xi,Xj)):
            if(len(csp.getDomain(Xi)) == 0):
                return False
            addArcs = arcs[Xi]

            for Xk in addArcs:  #<-- do the function thing
                q.put((Xk, Xi))
    return True








file = open("nickisdumb.txt", 'r')
inp = file.read()

if(len(inp) == 81):
    #call init CSP function
    # print("INP:", inp)
    # print("made it here")
    lool = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
    csp = CSP(lool)
    print("SUDOKU:")
    csp.printSudoku()
    AC3_A_BITCH(csp)