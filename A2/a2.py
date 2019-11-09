
import sys

fullDomain = [1,2,3,4,5,6,7,8,9]

class cell:
    def init(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value

class CSP:
    def __init__(self, inp):
        self.variables = [r + c for r in 'ABCDEFGHI' for c in '123456789']
        self.values = [int(val) for val in inp]
        self.domain = [(var, fullDomain if self.values[self.variables.index(var)] == 0 else self.values[self.variables.index(var)]) for var in self.variables]
        a = [self.colNeighbors(self.domain, i) for i in range(9)]
        print("A IS:~")
        print(a)
        print("----------")
        b = [self.rowNeighbors(self.domain, i) for i in range(9)]
        c = [self.cellNeighbors(self.domain, i, j) for i in range(9) for j in range(9)]

        self.neighbors = a+b+c #omegaLul
        # self.units = dict((s, [u[1] for u in self.neighbors if s in u[0]]) for s in self.variables)
        # for x in self.units:
        #     print(self.units[x])
        # print(self.units)


    # def nandDomain(pos,a,b,c):
    #     domain = []
    #     for i in range(1,10):
    #         for x in a:
    #             for y in b:
    #                 for z in c:
    #                     if(i not in x[1] and i not in y[1] and i not in z[1]):
    #                         if(i not in domain):
    #                             domain.append(i)
        

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
                # print("j+domCol:", j+domCol, "i+domRow:", i+domRow)
                # if(j+domCol != col or i+domRow != row):
                    # print("B POSITION:",(j+domCol) + (i+domRow)*9)
                    # print("B @ POSITION: ",b[(j+domCol) + (i+domRow)*9])
                    neighbors.append(b[(j+domCol) + (i+domRow)*9])
                    # print("cell is given cell")
        # print("I AM HEREEEEE")
        # print(neighbors)
        return neighbors


file = open("nickisdumb.txt", 'r')
inp = file.read()

if(len(inp) == 81):
    #call init CSP function
    print("INP:", inp)
    print("made it here")
    lool = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
    csp = CSP(lool)