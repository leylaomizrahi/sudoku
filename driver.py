import csv
import sys 
import Queue
import itertools
from sets import Set 
import time 

class CSP: 
    def __init__(self, name, value, domain, arcs = None): 
        self.name = name
        self.value = value
        self.domain = domain 
        self.arcs = []

    def update(self): 
        if len(self.domain) == 1: 
            self.value = self.domain[0]
            return True 
        return False 

    def printMe(self): 
        print "Square:" , self.name
        print "Value: " , self.value
        print "Domain: ", self.domain 

    def getarcs(self):
        a = []
        for x in self.arcs:
            a.append(x.name)
        return a 

def revise(value):
    revised = False
    equal = True
    for x in value[0].domain:
        for y in value[1].domain:
            if len(value[1].domain) == 1: 
                if x == y:
                    value[0].domain.remove(x)
                    revised = True
                    value[0].update()
    return revised

def makeArcs(V): 
    C0 = [[],[],[],[],[],[],[],[],[]]
    C1 = [[],[],[],[],[],[],[],[],[]]
    C2 = [[],[],[],[],[],[],[],[],[]]
    C = [C0,C1, C2]
    counter = 0
    j = 0
    for i in range(len(V)):
        C[0][j].append(V[i])
        counter = counter + 1
        if counter == 9:
            j = j + 1
            counter = 0

    j = 0
    for i in range(len(V)):
        C[1][j].append(V[i])
        j = j + 1
        if j == 9:
            j = 0

    i = 0
    k = 0

    for j in range(len(V)):
        C[2][k].append(V[i])
        C[2][k].append(V[i+1])
        C[2][k].append(V[i+2])
        C[2][k+1].append(V[i+3])
        C[2][k+1].append(V[i+4])
        C[2][k+1].append(V[i+5])
        C[2][k+2].append(V[i+6])
        C[2][k+2].append(V[i+7])
        C[2][k+2].append(V[i+8])
        if i == 18 or i == 45:
            k = k + 3
        if i == 72:
            break
        i = i + 9

    set = Set()

    for j in range(3):
        for i in range(9):
            for arc in itertools.combinations(C[j][i],2):
                if arc not in set:
                    set.add(arc)
                    arc[0].arcs.append(arc[1])
                    arc[1].arcs.append(arc[0])

    return C 


def Backtrack(V):
      assignment = []
      complete = True
      min = 10
      for x in V:
        assignment.append(x.value)
        if x.value == 0:
            complete = False
            if len(x.domain) <  min:
                min = x

      if complete == True:
          return assignment

      chosenone = min

      for i in range(len(chosenone.domain)):
          x = chosenone.domain[i]
          consistent = True
          for y in chosenone.arcs:
              if y.value == x:
                  consistent = False

          changed = []
          if consistent == True:
              trydis = True
              for others in chosenone.arcs:
                  for a in others.domain:
                      if a == x:
                          changed.append((others, list(others.domain)))
                          others.domain.remove(a)
                          if len(others.domain)== 0:
                              trydis = False

              if trydis == True:
                  chosenone.value = x
                  result = Backtrack(V)
                  if result != False:
                      return result
                  chosenone.value = 0

              for x in changed:
                  x[0].domain = x[1]

      return False


def AC3(V , C):        
    queue = Queue.Queue()
    set = Set() 

    for j in range(3): 
        for i in range(9): 
            for arc in itertools.combinations(C[j][i],2): 
                if arc not in set: 
                    set.add(arc)    
                    queue.put(arc)
                    queue.put((arc[1],arc[0]))

    while (queue.empty() != True):                                           
        value = queue.get()
        if revise(value):
            if (len(value[0].domain) == 0):
                print "Oops! Made a mistake on", value[0].name
                break
            for x in value[0].arcs:
                if x != value[1]:
                    queue.put((x, value[0]))

    result = [] 
    for x in V: 
        x.update
        result.append(x.value)
    found = True 
    for x in result: 
        if x == 0: 
            found = False

    if found == True: 
        return result 
    else: 
        return found 


def solveSudoku(Sudoku): 
    start = time.time()
    Letters = ['A','B','C','D','E','F','G','H','I']
    file_writer = csv.writer(open("output.txt", 'w'))
    Numbers = [1,2,3,4,5,6,7,8,9]
    Variables = []
  
    V = []

    for i in range(len(Letters)):
        for j in range(len(Numbers)):
            Variables.append((Letters[i],Numbers[j]))

    for i in range(len(Sudoku)):
        if Sudoku[i] == 0:
            D = [1,2,3,4,5,6,7,8,9]
            V.append(CSP(Variables[i],Sudoku[i], D))
        if Sudoku[i] != 0:
            Dfilled = [Sudoku[i]]
            V.append(CSP(Variables[i],Sudoku[i],Dfilled))
 

    C = makeArcs(V)
    result = AC3(V,C)
 
    if result == False: 
        result = Backtrack(V)
        print result 


    file_writer.writerow(result)

  #  print time.time() - start

#To test all sudoku puzzles 
#comment out this line                                                                                                                                                           
solveSudoku(list(map(int,sys.arv[1]))) 


#uncomment these lines 
#file_writer = csv.reader(open(sys.argv[1], 'r'))
#for row in file_writer: 
#    solveSudoku(list(map(int,row[0]))) 


                                         

