#strategy.py
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
class Strategy():
    def best_strategy(self, board, player, best_move, still_running):
        level = 1
        start = time.time()
        while time.time()-start<5:
            brd = ''.join(board).replace('?','').replace('@','X').replace('o','O')
            move = 'X' if player=='@' else 'O'
            mv = findBestMove(brd, move, level)
            mv1 = 11+(mv//8)*10+(mv%8)
            best_move.value = mv1
            level+=2

import time, sys
game = '...........................OX......XO...........................'
move = 'X'
if len(sys.argv) == 3:
    game = sys.argv[1]
    move = sys.argv[2]
elif len(sys.argv) == 2:
    game = sys.argv[1]

game = game.upper()
if len(sys.argv) == 2:
    if game.count('.') % 2 == 0:
        move = 'X'
    else:
        move = 'O'
move = move.upper()

def printBoard(game):
    print('\n'.join([game[i * 8:i * 8 + 8] for i in range(8)]))

borderTop = []
borderLeft = []
borderRight = []
borderBottom = []
for i in range(8): borderTop.append(i)
for i in range(8): borderLeft.append(i * 8)
for i in range(8): borderRight.append(i * 8 + 7)
for i in range(8): borderBottom.append(56 + i)

def wrapsAround(pos1, pos2):
    return pos1 in borderTop and pos2 in borderBottom or \
           pos1 in borderLeft and pos2 in borderRight or \
           pos1 in borderRight and pos2 in borderLeft or \
           pos1 in borderBottom and pos2 in borderTop

def returnValue(otherPos, iterator, current, game):
    if wrapsAround(current, current + iterator): return ''
    i = current + iterator
    while i in otherPos:
        if wrapsAround(i, i + iterator): break
        i += iterator

        if i < len(game) and i >= 0 and game[i] == '.':
            return i
    return ''

def legalMoves(game, move):
    if move == 'X':
        movePos = {i for i in range(64) if game[i] == 'X'}
        otherPos = {i for i in range(64) if game[i] == 'O'}
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
            if newInd>=0 and newInd<len(game) and game[newInd]==move:
                while newInd<len(game) and newInd>=0 and game[newInd]==move:
                    newInd+=i
                    if newInd in corner:
                        return True
    return False

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

    noCX = posMoves - CX(game, move)            ### only this can get to 73%
    if noCX: posMoves = noCX
    noEdge = posMoves - edge #########
    if noEdge: posMoves = noEdge

    return posMoves.pop()


adjInds = [1, -1, -8, 8, -9, -7, 7, 9]
def resultBoard(game, token, move):
    toRet = list(game[:])
    toRet[move] = token
    otherToken = 'X' if token == 'O' else 'O'
    toBeFilled = []
    for i in adjInds:
        if wrapsAround(move, move + i): continue
        pos = move + i
        while pos < 64 and pos >= 0 and game[pos] == otherToken:
            if wrapsAround(pos, pos + i): break
            toBeFilled.append(pos)
            pos += i
            if pos < len(game) and pos >= 0 and game[pos] == token:
                for i in toBeFilled:
                    toRet[i] = token
        toBeFilled = []
    return ''.join(toRet)

def evalBoard(board, token):
    otherToken = 'X' if token=='O' else 'O'
    myPoints = board.count(token)
    otherPoints = board.count(otherToken)
    return myPoints - otherPoints
def gameOver(board):
    if not legalMoves(board, 'X') and not legalMoves(board, 'O'): return True
    return False
def negamax(board, token, levels):
    if not levels: return [evalBoard(board, token)]
    if gameOver(board): return [evalBoard(board, token)]


    lm = legalMoves(board, token)
    otherToken = 'X' if token == 'O' else 'O'
    if not lm:
        nm = negamax(board, otherToken, levels - 1) + [-1]
        return [-nm[0]] + nm[1:]

    nmList = sorted([negamax(resultBoard(board, token, mv), otherToken, levels - 1) + [mv] for mv in lm])
    best = nmList[0]
    return [-best[0]] + best[1:]

n = 7

def findBestMove(game, move, level):
    if game.count('.') <= n:
        nm = negamax(game, move, -1)
        return nm[-1]  # returnMove(posMoves, game, move)))
    else:
        lm = legalMoves(game, move)
        for i in lm:  ### in corner
            if i in corner:
                return i
        for i in lm:  ### makes edge w corner
            if connectedToCorner(i, game, move):
                return i
        
        nm = negamax(game, move, level)
        return nm[-1]

    # nm = negamax(game, move, level)
    # return nm[-1]

def main():             ### Lab A
    n = 7
    if game.count('.') <= n:
        nm = negamax(game, move, -1)
        posMoves = legalMoves(game, move)
        print('Board:')
        printBoard(game)
        print('Possible Moves: ' + str(posMoves))
        print('My heuristic choice is {}'.format(returnMove(posMoves, game, move)))  # returnMove(posMoves, game, move)))
        print('Negamax is running with n = ' + str(game.count('.')))
        print('Negamax returns', nm, 'and my move is', nm[-1])
    else:
        posMoves = legalMoves(game, move)
        print('Board:')
        printBoard(game)
        print('Possible Moves:', posMoves)
        if len(posMoves) > 0: print('My heuristic choice is {}'.format(returnMove(posMoves, game, move)))

if __name__ == "__main__":        #########################3
    main()