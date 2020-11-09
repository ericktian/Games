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

import time
game = '...........................OX......XO...........................'
move = 'X'
# if len(sys.argv) == 3:
#     game = sys.argv[1]
#     move = sys.argv[2]
# elif len(sys.argv) == 2:
#     game = sys.argv[1]

game = game.upper()
# if len(sys.argv) == 2:
#     if game.count('.') % 2 == 0:
#         move = 'X'
#     else:
#         move = 'O'
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

### negamax
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
    otherToken = 'X' if token == 'O' else 'O'
    return board.count(token) - board.count(otherToken)

def negamax(board, token, levels):
    if not levels: return [evalBoard(board, token)]

    lm = legalMoves(board, token)
    otherToken = 'X' if token == 'O' else 'O'
    if not lm:
        nm = negamax(board, otherToken, levels - 1) + [-1]
        return [-nm[0]] + nm[1:]

    nmList = sorted([negamax(resultBoard(board, token, mv), otherToken, levels - 1) + [mv] for mv in lm])
    best = nmList[0]
    return [-best[0]] + best[1:]

# level = 1
# start = time.time()
# while time.time()-start<5:
#     nm = negamax(game, move, level)         ### levels = 1
#     print("At level", level, "nm gives", nm, "and I pick move", nm[-1])
#     level+=2

def findBestMove(game, move, level):
    # level = 3
    nm = negamax(game, move, level)
    # print("At level", level, "nm gives", nm, "and I pick move", nm[-1])
    return nm[-1]

# if __name__ == "__main__":        #########################3
#     main()