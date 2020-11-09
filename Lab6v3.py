### LAB 6 ###

### random values

#Othello is an 8*8 board with Xs, Os, and .s where . is an empty space
import sys, time, random
game = '...........................OX......XO...........................'
move = 'X'
if len(sys.argv) == 3:
    game = sys.argv[1]
    move = sys.argv[2]
elif len(sys.argv) == 2:
    game = sys.argv[1]

game = game.upper()
if len(sys.argv) == 2:
    if game.count('.')%2==0:
        move = 'X'
    else:
        move = 'O'
move = move.upper()

def printBoard(game):
    print('\n'.join([game[i*8:i*8+8] for i in range(8)]))

borderTop = []
borderLeft = []
borderRight = []
borderBottom = []
for i in range(8): borderTop.append(i)
for i in range(8): borderLeft.append(i*8)
for i in range(8): borderRight.append(i*8+7)
for i in range(8): borderBottom.append(56+i)

def wrapsAround(pos1, pos2):
    return pos1 in borderTop and pos2 in borderBottom or \
           pos1 in borderLeft and pos2 in borderRight or \
           pos1 in borderRight and pos2 in borderLeft or \
           pos1 in borderBottom and pos2 in borderTop

def returnValue(otherPos, iterator, current, game):
    if wrapsAround(current, current+iterator): return ''
    i = current + iterator
    while i in otherPos:
        if wrapsAround(i, i+iterator): break
        i += iterator

        if i<len(game) and i>=0 and game[i] == '.':
            return i
    return ''

def legalMoves(game, move):
    if move=='X':
        movePos = {i for i in range(64) if game[i]=='X'}
        otherPos = {i for i in range(64) if game[i]=='O'}
    else:
        movePos = {i for i in range(64) if game[i] == 'O'}
        otherPos = {i for i in range(64) if game[i] == 'X'}
    legal = set()
    for i in movePos:
        for x in [1, -1, -8, 8, -9, -7, 7, 9]:
            pos = returnValue(otherPos, x, i, game)
            if pos != '':
                legal.add(pos)

    return legal

### lab 6 stuff ###
corner = [0,7,56,63]
CorX = [[0,1,8,9], [7,6,14,15], [56,48,49,57], [63,54,55,62]]        ### first ind = ind of corner
edge = set()
for i in range(6):
    edge.add(i+1)
    edge.add(i+57)
    edge.add(8+i*8)
    edge.add(15+i*8)
def connectedToCorner(index, game, move):
    if index not in edge: return False
    if move=='X': otherMove='O'
    else: otherMove='X'
    otherPos = {i for i in range(64) if game[i]==otherMove}
    for i in [-1,1,-8,8]:
        if wrapsAround(index, i): continue
        newInd = index+i
        while newInd in otherPos:
            if wrapsAround(newInd, i): break
            newInd+=i
            if newInd in corner and game[newInd]==move:
                return True
    return False

# def CorXbad(game, index, move):
#     for i in CorX:
#         if index in i and game[i[0]]!=move:         ### i know this checks the corners, but doesn't matter since they've already been checked
#             return True
#     return False

def CX(game, move):         ### returns bad moves for c or x
    toRet = set()
    for i in CorX:
        if game[i[0]]!=move:
            for j in i[1:]: toRet.add(j)
    return toRet

def returnMove(posMoves, game, move):
    cornersToAdd = set()
    for i in posMoves:      ### in corner
        if i in corner:
            # return i
            cornersToAdd.add(i)
    if cornersToAdd: return random.choice([*cornersToAdd])
    edgesToAdd = set()
    for i in posMoves:      ### makes edge w corner
        if connectedToCorner(i, game, move):
            # return i
            edgesToAdd.add(i)
    if edgesToAdd: return random.choice([*edgesToAdd])
    # for i in posMoves:      ### checks for indices not at C or X or an edge
    #     if not CorXbad(game, i, move) and i not in edge:
    #         return i
    # for i in posMoves:      ### checks for indices not at C or X
    #     if not CorXbad(game, i, move):
    #         return i

    noCX = posMoves - CX(game, move)            ### only this can get to 73%
    if noCX: posMoves = noCX
    noEdge = posMoves - edge #########
    if noEdge: posMoves = noEdge

    return random.choice([*posMoves])#posMoves.pop()


posMoves = legalMoves(game, move)


# printBoard(game)
# print()
# listt = list(game)
# listt[returnMove(posMoves,game,move)] = '*'
# printBoard(''.join(listt))



if len(posMoves)>0: print(returnMove(posMoves, game, move))