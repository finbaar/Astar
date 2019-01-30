from priorityqueue import Priority_Queue
import copy

def nextState(state):
    """return the availavel state"""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                blankX = i
                blankY = j
                
    nextS = [(blankX+1,blankY),(blankX-1,blankY),(blankX,blankY+1),(blankX,blankY-1)]
    validS = []
    for item in nextS:
        if (item[0] >= 0 and item[0] < 3) and (item[1] >= 0 and item[1] < 3):
            tempS = list(map(list,state))
            x = state[item[0]][item[1]]
            tempS[blankX][blankY] = x
            tempS[item[0]][item[1]] = 0

            validS.append(list(map(list,tempS)))

    return validS


def hFrist(validS):
    global goal
    current = (1000000,[])
    for item in validS:
        misplaced = 0
        for i in range(3):
            for j in range(3):
                if item[i][j] != goal[i][j]:
                    misplaced += 1
        if misplaced < current[0]:
            current = (misplaced,(list(map(list,item))))  
    return current

def hSecond(validS):
    global goal
    current = (100000000, [])
    for item in validS:
        step = 0
        for i in range(3):
            for j in range(3):
                k = item[i][j]
                for x in range(3):
                    for y in range(3):
                        if goal[x][y] == k:
                            step += abs(((x-i) + (y-j)))
        if step < current[0]:
            current = (step, (list(map(list,item))))
    return current 

def nextMove(state, first = True):
    nextS = nextState(state)
    if first:
        return hFrist(nextS)
    else:
        return hSecond(nextS)


print("1,2,3\n4,5,6\n7,8,0\n-------")
start = []
goal = []
for i in range(3):
    temp = input().split(',')
    start.append([int(temp[0]), int(temp[1]), int(temp[2])])

for i in range(3):
    temp = input().split(',')
    goal.append([int(temp[0]), int(temp[1]), int(temp[2])])

current = copy.deepcopy(start)
 
while current != goal:
    nextS = nextMove(current)
    print("The cost is " + str(nextS[0]))
    print(nextS[1])
    current = copy.deepcopy(nextS[1])













