from priorityqueue import Priority_Queue
import math

def nextState(aState):
    """return the availavel state"""
    state = aState.st
    #find the moveable piece
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                blankX = i
                blankY = j
                break
    #           index 0                index 1              index 2             index 3
    #assigning number to each possible state, so it won't go back
    nextS = [(blankX+1,blankY,1),(blankX-1,blankY,0),(blankX,blankY-1,3),(blankX,blankY+1,2)]
    
    #remember where it comes from, and delete the state which may go back to previouse state
    if aState.ls != 4:
        del nextS[aState.ls]

    validS = []
    #check whether or not the reamining state is valid,make sure it won't move out
    for item in nextS:
        if (item[0] >= 0 and item[0] < 3) and (item[1] >= 0 and item[1] < 3):
            tempS = list(map(list,state))
            x = state[item[0]][item[1]]
            tempS[blankX][blankY] = x
            tempS[item[0]][item[1]] = 0
            #if if valid, creat the object and append it into the list
            validS.append(State(aState.key, list(map(list,tempS)), item[2], aState.step+1))

    return validS


def hFrist(validS):
    global goal
    """hamming distance heuristic"""
    for itemState in validS:
        item = itemState.st
        misplaced = 0
        for i in range(3):
            for j in range(3):
                if item[i][j] != goal[i][j]:
                    misplaced += 1
        itemState.key = (itemState.step + misplaced)
    return validS

def hSecond(validS):
    global goal
    """manhattan distance heuristic
    """
    for itemState in validS:
        item = itemState.st
        step = 0
        for i in range(3):
            for j in range(3):
                k = item[i][j]
                for x in range(3):
                    for y in range(3):
                        if goal[x][y] == k:
                            step += (abs(x-i) + abs(y-j))
                            #the mistate make in hSecond, causes a lot of more work
                            #step += abs(((x-i) + (y-j)))
        itemState.key = (step + itemState.step)
    
    return validS

def hThird(validS):
    """heuristic thiree, take the acutual distance as cose function, with diagnose, we don't use 
        a + b, insted the cost become sqt(a**2 + b**2)
    """
    for itemState in validS:
        item = itemState.st
        step = 0
        for i in range(3):
            for j in range(3):
                k = item[i][j]
                for x in range(3):
                    for y in range(3):
                        if goal[x][y] == k:
                            """the search cost is less, but it's not the optimal one"""
                            #admissible heuristic, 
                            #step += ((abs(x-i))**2 + (abs(y-j))**2)

                            #this one is better than heuristic one but worse than heuristic two
                            step += math.sqrt((abs(x-i))**2 + (abs(y-j))**2)

        itemState.key = (step + itemState.step)
    
    return validS

def nextMove(state, first = False):
    """combine the state function and heuristic funtion
       the frist deteminte whether run the first heuristic or second
    """
    nextS = nextState(state)
    if first:
        return hFrist(nextS)
    else:
        return hSecond(nextS)


class State:
    def __init__(self, k,st,last, step):
        """this State has 4 arrtibues
            key stands for the heuristic cost + the step cost
            st stands for the puzzle's state
            ls stands for how does it changed from last state, either top,down,right or left.
            step stands for the step cost from the start state to current state
        """
        self.key = k
        self.st = st
        self.ls = last
        self.step = step

    def precede(self, x):
        return self.key < x.key   # do not use <= or >=

    def assign(self, v):  # v must be of higher priority value than the current key
        x = State(v, self.st, self.ls,self.step)  # x is a local temporary instance
        if not self.precede(x):
            self.key = v
            return True
        else:
            return False

def showPuzzle(arr):
    """a function to print the puzzle nicely"""
    for i in range(3):
        for j in range(3):
            print(str(arr[i][j]) + " ", end='')
        print()

print("1,2,3\n4,5,6\n7,8,0\n-------")
start = []
goal = []

#obtaining the start state
for i in range(3):
    temp = input().split(',')
    start.append([int(temp[0]), int(temp[1]), int(temp[2])])

#obtaining the goal state
for i in range(3):
    temp = input().split(',')
    goal.append([int(temp[0]), int(temp[1]), int(temp[2])])

startS = State(0, start,4,0)

pq = Priority_Queue()
pq.enqueue(startS)

path = {}
finalState = None

count = 0
while pq:
    current = pq.dequeue()
    count += 1
    if current.st == goal:
        finalState = current
        print("The total cost is " + str(current.step))
        #showPuzzle(current.st)
        break
    else:
        #print("The cost is " + str(current.step))
        #showPuzzle(current.st)
        nextS = nextMove(current)
        for item in nextS:
            pq.enqueue(item)
            #remebering where it comes from and store it as a dictonary
            path[item] = current

print("total search is " + str(count))


current = finalState
ret = []
ret.append(goal)
count = 0
# get the puzzle from goal back to the start
while current.st != start:
    current = path[current]
    ret.append(current.st)
    count += 1
    if count == 100000:
        print("wrong")

# print the puzzle from start to goal
count = 0
for i in range(len(ret)-1, -1, -1):
    print("\nstep " + str(count) + " is:")
    count += 1
    showPuzzle(ret[i])

    




