
import sys
import queue
import copy

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
                self.values[x] = [int(inp[index])]
            index+=1
        print(self.values)
        self.arcs = {}
        index = 0
        for x in range(0,9):
            for y in range(0,9):
                
                self.arcs[xPos[x] + yPos[y]] = self.setArcs(x,y)
                index += 1
        
        print("ARCS:")
        print(self.arcs)
        

    def printSudoku(self):
        dash = "------------"
        line = ""
        counter = 0
        for y in range(0,9):
            if(y % 3  == 0):
                print(dash)
            for x in range(0,9):
                if(x%3 == 0):
                    line+='|'
                line+= self.inp[counter]
                counter+=1

            print(line+'|')
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

    def isSolved(self):
        result = True
        for d in self.values.values():
            if(len(d) > 1):
                result = False
                break
        return result

    def cloneValues(self):
        values = {}
        for key in self.values.keys():
            newValues = []
            for nextValue in self.values[key]:
                newValues.append(nextValue)
            values[key] = newValues
        return values


    def getValues(self):
        return self.values

    def getVariables(self):
        return self.variables

    def getArcs(self):
        return self.arcs
    def getNeighbors(self, Xi):
        result = []
        for (x,y) in self.arcs[Xi]:
            result.append(y)
        print(result)
        return result

    def getDomain(self, Xi):
        return self.values[Xi]
    def removeFromDomain(self, Xi, i):
        self.values[Xi].remove(i)
    def revision(self, Xi, Xj):
        i = 0
        # print("XI:",Xi)
        # print("Xj:", Xj)
        
        domXi = self.values[Xi] #get domain of Xi eg. 'A1'
        # print(domXi)
        # print("Xi:",domXi)
        # print("Xj:", self.values[Xj])
        isRevised = False
        for x in domXi:
            # print("for x")
            invalid = True
            
            for y in self.values[Xj]:
                # print("for y")
                # print("X:",x,"Y:",y)
                if x != y:
                    invalid = False
            if invalid:
                print("inalid. Xi:",Xi,"i:",i)
                print(domXi)
                domXi.pop(1)
                isRevised = True
            else:
                i += 1
        return isRevised

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
        

    # def colNeighbors(self, b, col):
    #     neighbors = []
    #     for i in range(col, len(b), 9):
    #         neighbors.append(b[i])

    #     return neighbors

    # def rowNeighbors(self, b, row):
    #     neighbors = []
    #     end = (row + 1) * 9
    #     start = end - 9
    #     for i in range(start, end, 1):
    #         neighbors.append(b[i])

    #     return neighbors
    # def cellNeighbors(self, b, row, col):
    #     # print("R:", row, "C:", col)
    #     neighbors = []
    #     domRow = row - row % 3
    #     domCol = col - col % 3
    #     for j in range(3):
    #         for i in range(3):
    #                 neighbors.append(b[(j+domCol) + (i+domRow)*9])
    #     return neighbors


#revision algorithm. reduces domain of Xi based on constraints


class BTS():
    def __init__(self, csp):
        self.csp = csp
        self.unassigned = {}
        self.useAC3 = True
        
        for key in self.csp.values.keys():
            
            values = self.csp.values[key]
            print(values)
            self.unassigned[key] = True if len(values) != 1 else False
        
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

        savedData = {}
        savedData[key] = copy.copy(self.csp.values[key])
        self.unassigned[key] = False
        self.csp.values[key] = [value]
        for Xk in self.csp.getValues[key]:
            index = 0
            domain = self.csp.values[key]
            copied = False
            for dValue in domain:
                if (dValue == value):
                    if not copied:
                        savedData[Xk] = copy.copy(domain)
                        copied = True
                    domain.pop(index)
                else:
                    index+=1
        return savedData

    def search(self, depth):
        if(self.csp.isSolved()):
            return True
        
        (key, values) = self.unassignedValues()
        for value in values:
            if self.testConsistency(key, value):
                if self.useAC3:
                    savedValues = self.csp.cloneValues()
                    self.csp.values[key] = [value]
                    self.unassigned[key] = False
                    ac3 = AC3_A_BITCH(self.csp)
                    # ac3.solve()
                else:
                    savedData = self.forwardCheck(key, value)
                
                if(self.search(depth+1)):
                    return True
                if(self.useAC3):
                    self.unassigned[key] = True
                    self.csp.values = savedValues
                else:
                    for nextKey in savedData.keys():
                        self.csp.values[nextKey] = savedData[nextKey]
        return False

    def solve(self):
        return self.search(1)




def AC3_A_BITCH(csp):
    q = queue.Queue()
    arcs = csp.getArcs()
    variables = csp.getVariables()

    # print("HERE:")
    # print(arcs)
    for var in variables:
        a = arcs[var]
        for arc in a:
            
            q.put((var,arc))
    # print("finished")
    print("QUEUE:")
    print(list(q.queue))
    #GET ARCS -  call the function boi
    #GET NEIGHBORS - call function
    while not q.empty():
        (Xi, Xj) = q.get()
        if(csp.revision(Xi,Xj)):
            if(len(csp.values[Xi]) == 0):
                return False
            addArcs = arcs[Xi]

            for Xk in csp.getNeighbors(Xi):  #<-- do the function thing

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
    if(csp.isSolved() == True):
        print("sudoku was already solved. that was easy.")
    else:
        print("SUDOKU:")
        csp.printSudoku()
        bts = BTS(csp)
        bts.solve()
        bts.csp.printSudoku()