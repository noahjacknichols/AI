
import sys

class CSP:
    def __init__(self, inp):
        fullDomain = [1,2,3,4,5,6,7,8,9]
        counter = 0
        arr = [[0] * 9 for i in range(9)]
        # print(arr)
        for i in range(len(arr)):
            for j in range(len(arr)):
                arr[i][j] = int(inp[counter])
                counter+=1
                # print(counter)
        print(arr)
        self.variables = arr
        domain = [[[]] * 9 for i in range(9)]
        CSP.domain = domain
        # print("SELF VARIABLES:")
        # print(self.variables)
        for j in range(len(self.variables)):
            for i in range(len(self.variables)):
                print(self.variables[j][i])
                if(self.variables[j][i] != 0):
                    #variables[i][j] is between 1-9
                    print("1-9")
                    self.domain[j][i] = [self.variables[j][i]]

                else:
                    #value is 0 check row, col, 3x3
                    print("value is not 1-9")
                    a = self.checkCol(self.variables[j][i], i, j)
                    b = self.checkRow(self.variables[j][i], i, j)
                    c = self.check3x3(self.variables[j][i], i, j)
                    print("A:", a, "\nB:", b, "\nC:", c)
                    self.domain[j][i] = list(set(fullDomain) - set(a) - set(b) - set(c))
        for i in range(9):
            print(self.variables[i])
        print("DOMAIN IS:")
        print(domain[0][0])



    def checkCol(self, b, row, col):
        return [self.variables[i][row] for i in range(len(self.variables[row]))]
    
    def checkRow(self, b, row, col):
        return self.variables[col]
    
    def check3x3(self, b, row, col):
        domain = []
        domRow = row - row % 3
        domCol = col - col % 3
        for i in range(3):
            for j in range(3):
                domain.append(self.variables[i+domCol][j+domRow])
        
        return domain

    
    # def setDomain(self):
    #     arr = self.variables
    #     domain = [1,2,3,4,5,6,7,8,9]
    #     valuesSeen = []
    #     for i in range(len(arr)):
    #         for j in range(len(arr)):
    #             if(int(arr[i][j]) not in valuesSeen):
    #                 valuesSeen.append(int(arr[i][j]))
    #         for x in domain:
    #             if(domain[x] not in valuesSeen):
    #                 self.domain[i].append(domain[x])
    #         valuesSeen = []
        





file = open("nickisdumb.txt", 'r')
inp = file.read()

if(len(inp) == 81):
    #call init CSP function
    print("INP:", inp)
    print("made it here")
    csp = CSP(inp)