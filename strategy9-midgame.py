#
# Erick Tian

# not that good w midgame, 60-70%


EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'


class Strategy():
    def best_strategy(self, board, player, best_move, still_running):
        level = 4
        start = time.time()
        brd = ''.join(board).replace('?', '').replace('@', 'X').replace('o', 'O')
        move = 'X' if player == '@' else 'O'
        posMoves = legalMoves(brd, move)
        best_move.value = returnMove(set(posMoves), brd, move)
        while time.time() - start < 5:
            mv = findBestMove(brd, move, level)
            mv1 = 11 + (mv // 8) * 10 + (mv % 8)
            best_move.value = mv1
            level += 1

def debugBoard(game, moves):
    listgame = list(game)
    for i in moves:
        listgame[i] = '*'
    return ''.join(listgame)


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

adjInds = [1, -1, -8, 8, -9, -7, 7, 9]

def legalMoves(game, move):
    otherMove = 'X' if move == 'O' else 'O'
    movePos = set()
    otherPos = set()
    dotPos = set()
    for i in range(64):
        if game[i]==move: movePos.add(i)
        elif game[i]==otherMove: otherPos.add(i)
        elif game[i]=='.': dotPos.add(i)

    legal = {}
    for i in dotPos:
        for x in adjInds:
            pos = ''
            flip = set()
            if not wrapsAround(i, i+x):
                c = i+x
                while c in otherPos:
                    flip.add(c)
                    if wrapsAround(c, c+x):
                        break
                    c += x
                    if c<len(game) and c>=0 and c in movePos:
                        pos = i
            if pos != '':
                # legal.add(pos)
                if pos in legal: legal[pos].update(flip)
                else: legal[pos] = flip
    return legal

def resultBoard(game, token, move, lm):
    toRet = list(game)
    toRet[move] = token
    for i in lm[move]:
        toRet[i] = token
    return ''.join(toRet)

### lab 6 stuff ###
corner = [0, 7, 56, 63]
CorX = [[0, 1, 8, 9], [7, 6, 14, 15], [56, 48, 49, 57], [63, 54, 55, 62]]  ### first ind = ind of corner
edge = set()
for i in range(6):
    edge.add(i + 1)
    edge.add(i + 57)
    edge.add(8 + i * 8)
    edge.add(15 + i * 8)


def connectedToCorner(index, game, move):
    if index not in edge: return False
    if move == 'X':
        otherMove = 'O'
    else:
        otherMove = 'X'
    otherPos = {i for i in range(64) if game[i] == otherMove}
    for i in [-1, 1, -8, 8]:
        if wrapsAround(index, i): continue
        newInd = index + i
        while newInd in otherPos:
            if wrapsAround(newInd, i): break
            newInd += i
            if newInd in corner and game[newInd] == move:
                return True
            if newInd >= 0 and newInd < len(game) and game[newInd] == move:
                while newInd < len(game) and newInd >= 0 and game[newInd] == move:
                    newInd += i
                    if newInd in corner:
                        return True
    return False


def CX(game, move):  ### returns bad moves for c or x
    toRet = set()
    for i in CorX:
        if game[i[0]] != move:
            for j in i[1:]: toRet.add(j)
    return toRet


def returnMove(posMoves, game, move):
    for i in posMoves:  ### in corner
        if i in corner:
            return i
    for i in posMoves:  ### makes edge w corner
        if connectedToCorner(i, game, move):
            return i

    noCX = posMoves - CX(game, move)  ### only this can get to 73%
    if noCX: posMoves = noCX
    noEdge = posMoves - edge  #########
    if noEdge: posMoves = noEdge

    return posMoves.pop()

def evalBoard(board, token):
    otherToken = 'X' if token == 'O' else 'O'
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

    nmList = sorted([negamax(resultBoard(board, token, mv, lm), otherToken, levels - 1) + [mv] for mv in lm])
    best = nmList[0]
    return [-best[0]] + best[1:]

def negamaxTerminal(brd, token ,improvable, hardBound):
    enemy = 'X' if token == 'O' else 'O'
    lm = legalMoves(brd, token)
    if not lm:
        lm = legalMoves(brd, enemy)
        if not lm: return [evalBoard(brd, token)] ### game over
        nm = negamaxTerminal(brd, enemy, -hardBound, -improvable) + [-1]
        return [-nm[0]] + nm[1:]
    best = []
    newHB = -improvable
    for mv in lm:
        nm = negamaxTerminal(resultBoard(brd, token, mv, lm), enemy, -hardBound, newHB) + [mv]
        if not best or nm[0]<newHB:
            best = nm
            if nm[0]<newHB:
                newHB = nm[0]
                if -newHB>hardBound: return [-best[0]] + best[1:]
    return [-best[0]] + best[1:]

center = [27,28,35,36]
cMoves = [9,14,49,54]
adj = [[8, 1, 9], [0, 2, 8, 9, 10], [1, 3, 9, 10, 11], [2, 4, 10, 11, 12], [3, 5, 11, 12, 13], [4, 6, 12, 13, 14],
       [5, 7, 13, 14, 15], [15, 14, 6], [0, 1, 9, 16, 17], [0, 1, 2, 8, 10, 16, 17, 18], [1, 2, 3, 9, 11, 17, 18, 19],
       [2, 3, 4, 10, 12, 18, 19, 20], [3, 4, 5, 11, 13, 19, 20, 21], [4, 5, 6, 12, 14, 20, 21, 22], [5, 6, 7, 13, 15, 21, 22, 23],
       [6, 7, 14, 22, 23], [8, 9, 17, 24, 25], [8, 9, 10, 16, 18, 24, 25, 26], [9, 10, 11, 17, 19, 25, 26, 27], [10, 11, 12, 18, 20, 26, 27, 28],
       [11, 12, 13, 19, 21, 27, 28, 29], [12, 13, 14, 20, 22, 28, 29, 30], [13, 14, 15, 21, 23, 29, 30, 31], [14, 15, 22, 30, 31], [32, 33, 16, 17, 25],
       [32, 33, 34, 16, 17, 18, 24, 26], [33, 34, 35, 17, 18, 19, 25, 27], [34, 35, 36, 18, 19, 20, 26, 28], [35, 36, 37, 19, 20, 21, 27, 29],
       [36, 37, 38, 20, 21, 22, 28, 30], [37, 38, 39, 21, 22, 23, 29, 31], [38, 39, 22, 23, 30], [33, 40, 41, 24, 25], [32, 34, 40, 41, 42, 24, 25, 26],
       [33, 35, 41, 42, 43, 25, 26, 27], [34, 36, 42, 43, 44, 26, 27, 28], [35, 37, 43, 44, 45, 27, 28, 29], [36, 38, 44, 45, 46, 28, 29, 30],
       [37, 39, 45, 46, 47, 29, 30, 31], [38, 46, 47, 30, 31], [32, 33, 41, 48, 49], [32, 33, 34, 40, 42, 48, 49, 50], [33, 34, 35, 41, 43, 49, 50, 51],
       [34, 35, 36, 42, 44, 50, 51, 52], [35, 36, 37, 43, 45, 51, 52, 53], [36, 37, 38, 44, 46, 52, 53, 54], [37, 38, 39, 45, 47, 53, 54, 55],
       [38, 39, 46, 54, 55], [40, 41, 49, 56, 57], [40, 41, 42, 48, 50, 56, 57, 58], [41, 42, 43, 49, 51, 57, 58, 59], [42, 43, 44, 50, 52, 58, 59, 60],
       [43, 44, 45, 51, 53, 59, 60, 61], [44, 45, 46, 52, 54, 60, 61, 62], [45, 46, 47, 53, 55, 61, 62, 63], [46, 47, 54, 62, 63], [48, 57, 49],
       [48, 49, 50, 56, 58], [49, 50, 51, 57, 59], [50, 51, 52, 58, 60], [51, 52, 53, 59, 61], [52, 53, 54, 60, 62], [53, 54, 55, 61, 63], [54, 55, 62]]

def evalBoardStart(board, token):
    otherToken = 'X' if token == 'O' else 'O'
    movePos = set()
    otherPos = set()
    dotPos = set()
    for i in range(64):
        if board[i] == move:
            movePos.add(i)
        elif board[i] == otherToken:
            otherPos.add(i)
        elif board[i] == '.':
            dotPos.add(i)

    myPoints = 0
    otherPoints = 0
    for i in movePos:
        # for k in adj[i]:
        #     if board[k] == '.': myPoints -= 3               # check for frontier moves
        #     elif board[k] == token: myPoints += 1           # check for grouped moves
        if i in center:
            myPoints += 15
        elif i in corner:
            myPoints += 500
        elif i in edge:
            myPoints -= 3
        elif i in cMoves:
            myPoints -= 10
        else:
            myPoints -= 1
    for i in otherPos:
        # for k in adj[i]:
        #     if board[k] == '.': otherPoints -= 3
        #     # elif board[k] == otherToken: otherPoints += 1
        if i in center:
            otherPoints += 15
        elif i in corner:
            otherPoints += 500
        elif i in edge:
            otherPoints -= 3
        elif i in cMoves:
            otherPoints -= 10
        else:
            otherPoints -= 1

    return myPoints - otherPoints

def negamaxStart(board, token, levels):
    if not levels: return [evalBoardStart(board, token)]
    if gameOver(board): return [evalBoardStart(board, token)]

    lm = legalMoves(board, token)
    otherToken = 'X' if token == 'O' else 'O'
    if not lm:
        nm = negamax(board, otherToken, levels - 1) + [-1]
        return [-nm[0]] + nm[1:]

    nmList = sorted([negamax(resultBoard(board, token, mv, lm), otherToken, levels - 1) + [mv] for mv in lm])
    best = nmList[0]
    return [-best[0]] + best[1:]

nextToCE = {2,10,16,17,18, 5,13,21,22,23, 40,41,42,50,58, 45,46,47,53,61}

def evalBoardMid(board, token):
    otherToken = 'X' if token == 'O' else 'O'
    movePos = set()
    otherPos = set()
    dotPos = set()
    for i in range(64):
        if board[i] == move:
            movePos.add(i)
        elif board[i] == otherToken:
            otherPos.add(i)
        elif board[i] == '.':
            dotPos.add(i)

    myPoints = 0
    otherPoints = 0
    for i in movePos:
        if i in center:
            myPoints += 15
        elif i in corner:
            myPoints += 500
        elif connectedToCorner(i, board, token):
            myPoints += 50
        elif i in nextToCE:
            myPoints += 10
        elif i in cMoves:
            myPoints -= 20
        else:
            myPoints += 5
    for i in otherPos:
        if i in center:
            otherPoints += 15
        elif i in corner:
            otherPoints += 500
        elif connectedToCorner(i, board, otherToken):
            otherPoints += 50
        elif i in nextToCE:
            myPoints += 10
        elif i in cMoves:
            otherPoints -= 20
        else:
            otherPoints += 5

    return myPoints - otherPoints
def negamaxMid(board, token, levels):
    if not levels: return [evalBoardMid(board, token)]
    if gameOver(board): return [evalBoardMid(board, token)]

    lm = legalMoves(board, token)
    otherToken = 'X' if token == 'O' else 'O'
    if not lm:
        nm = negamax(board, otherToken, levels - 1) + [-1]
        return [-nm[0]] + nm[1:]

    nmList = sorted([negamax(resultBoard(board, token, mv, lm), otherToken, levels - 1) + [mv] for mv in lm])
    best = nmList[0]
    return [-best[0]] + best[1:]

def findBestMove(game, move, level):
    # if game.count('.') <= n and level!=1:
    #     nm = negamaxTerminal(game, move, -65, 65)
    #     return nm[-1]  # returnMove(posMoves, game, move)))
    # else:
    #     lm = legalMoves(game, move)
    #     for i in lm:  ### in corner
    #        if i in corner:
    #            return i
    #     for i in lm:  ### makes edge w corner
    #        if connectedToCorner(i, game, move):
    #            return i
    #
    #     nm = negamax(game, move, level)
    #     return nm[-1]

    dots = game.count('.')

    if dots >= 50:
        nm = negamaxStart(game, move, level)  # lvl start @ 4 and increase
        return nm[-1]
    elif dots <= n:
        nm = negamaxTerminal(game, move, -65, 65)
        return nm[-1]
    else:  # level start @
        nm = negamaxMid(game, move, level)
        return nm[-1]

n = 11

def main():
    dots = game.count('.')
    posMoves = legalMoves(game, move)
    print('Possible Moves: ' + str(set(posMoves)))
    print('My heuristic choice is {}'.format(returnMove(set(posMoves), game, move)))
    print('Board:')
    printBoard(game)
    timeS = time.time()
    lvl = 4
    while time.time()-timeS < 5:
        if dots >=50:
            nm = negamaxStart(game, move, lvl)        #lvl start @ 4 and increase
            print(nm, nm[-1])
        elif dots <= n:
            nm = negamaxTerminal(game, move, -65, 65)
            print('Negamax is running with n = ' + str(game.count('.')))
            print('Negamax returns', nm, 'and my move is', nm[-1])
        else:                                     #level start @
            nm = negamaxMid(game, move, lvl)
            print(nm, nm[-1])
        lvl += 1
    # if dots <50 and dots >11:
    #     nm = negamaxMid(game, move, 4)
    #     print(nm, nm[-1])

if __name__ == "__main__":
    main()

