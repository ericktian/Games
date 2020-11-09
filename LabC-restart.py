# strategy.py
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'


class Strategy():
    def best_strategy(self, board, player, best_move, still_running):
        level = 1
        start = time.time()
        while time.time() - start < 5:
            brd = ''.join(board).replace('?', '').replace('@', 'X').replace('o', 'O')
            move = 'X' if player == '@' else 'O'
            mv = findBestMove(brd, move, level)
            mv1 = 11 + (mv // 8) * 10 + (mv % 8)
            best_move.value = mv1
            level += 2


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


def debugBoard(game, moves):
    listgame = list(game)
    for i in moves:
        listgame[i] = '*'
    return ''.join(listgame)


def wrapsAround(pos1, pos2):
    return pos1 in borderTop and pos2 in borderBottom or \
           pos1 in borderLeft and pos2 in borderRight or \
           pos1 in borderRight and pos2 in borderLeft or \
           pos1 in borderBottom and pos2 in borderTop


# def returnValue(otherPos, iterator, current, game):
#     if wrapsAround(current, current + iterator): return ''
#     i = current + iterator
#     while i in otherPos:
#         if wrapsAround(i, i + iterator): break
#         i += iterator
#
#         if i < len(game) and i >= 0 and game[i] == '.':
#             return i
#     return ''

adjInds = [1, -1, -8, 8, -9, -7, 7, 9]

def legalMoves(game, move):
    otherMove = 'X' if move == 'O' else 'O'
    movePos = {i for i in range(64) if game[i] == move}
    otherPos = {i for i in range(64) if game[i] == otherMove}
    legal = {}
    for i in movePos:
        for x in adjInds:
            pos = ''

            toBeFilled = set()
            if not wrapsAround(i, i + x):
                current = i + x
                while current in otherPos:
                    toBeFilled.add(current)

                    if wrapsAround(current, current + x) or current+x>=len(game) or current+x<0:
                        break
                    if game[current+x] == '.':
                        pos = current+x
                    current += x

            if pos != '':
                if pos in legal: legal[pos].update(toBeFilled)
                else: legal[pos] = toBeFilled

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

n = 15


def findBestMove(game, move, level):
    if game.count('.') <= n and level!=1:
        nm = negamaxTerminal(game, move, -65, 65)
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


def main():
    if game.count('.') <= n:
        posMoves = legalMoves(game, move)
        print('Board:')
        printBoard(game)
        print('Possible Moves: ' + str(set(posMoves)))
        print('My heuristic choice is {}'.format(returnMove(set(posMoves), game, move)))  # returnMove(posMoves, game, move)))
        nm = negamaxTerminal(game, move, -65, 65)
        print('Negamax is running with n = ' + str(game.count('.')))
        print('Negamax returns', nm, 'and my move is', nm[-1])
    else:
        posMoves = set(legalMoves(game, move))
        print('Board:')
        printBoard(game)
        print('Possible Moves:', posMoves)
        if len(posMoves) > 0: print('My heuristic choice is {}'.format(returnMove(posMoves, game, move)))

if __name__ == "__main__":
    main()