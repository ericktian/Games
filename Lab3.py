#Othello is an 8*8 board with Xs, Os, and .s where . is an empty space
import sys

### Set game, token, movelist
arglen = len(sys.argv)
game,token,movelist = '...........................OX......XO...........................','X',[]
if arglen>1:
    if len(sys.argv[1])==64:
        game = sys.argv[1].upper()
        arglist = sys.argv[2:]
    else: arglist = sys.argv[1:]
    if len(arglist) and arglist[0].upper() in ['X','O']:
        token = arglist[0].upper()
        arglist = arglist[1:]
    else:
        token = 'X' if game.count('.')%2==0 else 'O'
    movelist = [i.upper() for i in arglist[:]]
    for i in range(len(movelist)):
        if movelist[i][0] in 'ABCDEFGH':            ### convert a1 to 0
            movelist[i] = (int(movelist[i][1])-1)*8 + ord(movelist[i][0])-65
        else: movelist[i] = int(movelist[i])

### Methods
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

adjInds = [1,-1,-8,8,-9,-7,7,9]

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
        for x in adjInds:
            pos = returnValue(otherPos, x, i, game)
            if pos != '':
                legal.add(pos)
    return legal

def resultBoard(game, token, move):
    toRet = list(game[:])
    toRet[move] = token
    otherToken = 'X' if token=='O' else 'O'
    toBeFilled = []
    for i in adjInds:
        if wrapsAround(move, move+i): continue
        pos = move + i
        while pos<64 and pos>=0 and game[pos]==otherToken:
            if wrapsAround(pos, pos+i): break
            toBeFilled.append(pos)
            pos += i
            if pos<len(game) and pos>=0 and game[pos]==token:
                for i in toBeFilled:
                    toRet[i] = token
        # if i == -1:
        #     print(toBeFilled)
        toBeFilled = []
    return ''.join(toRet)

### Start
# print('\n-----START-----\n\n2D Board:')
printBoard(game)
# print('1D Board:\n'+game)
print(game+'\n'+str(game.count('X'))+'/'+str(game.count('O'))+'\n')

### Moves
if len(movelist):
    # print('\n-----MOVES-----\n')
    currToken = 'X' if token == 'O' else 'O'    #intentionally put the wrong token; will be fixed in loop
    result = game
    for i in range(len(movelist)):
        currToken = 'X' if currToken == 'O' else 'O'    #fixed here
        if not legalMoves(result, currToken):
            currToken = 'X' if currToken == 'O' else 'O'
        if not legalMoves(result, currToken):
            print('No more possible moves. Game over.')
            print('List of moves:', ', '.join([str(i) for i in movelist[:i]]))
            exit()

        print('Move:', currToken, '@', movelist[i])#, '\nToken:', currToken, '\n2D Board:')
        result = resultBoard(game, currToken, movelist[i])
        printBoard(result)
        # print('1D Board:\n'+result+'\n')
        print(result, str(result.count('X'))+'/'+str(result.count('O'))+'\n')
        game = result

    print('List of moves:', ', '.join([str(i) for i in movelist]))