### LAB 6 ###

#Othello is an 8*8 board with Xs, Os, and .s where . is an empty space
import sys, time
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
    # if game[0]==move and sum(game[i]==otherMove for i in borderTop[:index])==0
    otherPos = {i for i in range(64) if game[i]=='O'} if move=='X' else {i for i in range(64) if game[i]=='X'}
    for x in [1,-1,-8,8]:
        pos = returnValue(otherPos, x, index, game)
        if pos in corner:
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
    for i in posMoves:      ### in corner
        if i in corner:
            return i
    for i in posMoves:      ### makes edge w corner
        if connectedToCorner(i, game, move):
            return i
    # for i in posMoves:      ### checks for indices not at C or X or an edge
    #     if not CorXbad(game, i, move) and i not in edge:
    #         return i
    # for i in posMoves:      ### checks for indices not at C or X
    #     if not CorXbad(game, i, move):
    #         return i

    # noCX = posMoves - CX(game, move)
    # if noCX: posMoves = noCX
    # noEdge = posMoves - edge
    # if noEdge: posMoves = noEdge

    return posMoves.pop()


posMoves = legalMoves(game, move)

if len(posMoves)>0: print(returnMove(posMoves, game, move))