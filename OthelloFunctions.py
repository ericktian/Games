#Othello is an 8*8 board with Xs, Os, and .s where . is an empty space
import sys, time
game = '...........................OX......XO...........................'
move = 'X'
if len(sys.argv) == 3:
    game = sys.argv[1]
    move = sys.argv[2]
elif len(sys.argv) == 2:
    game = sys.argv[1]

# listUpper = []
# for i in range(len(game)):
#     listUpper.append(game[i].toUpper())
# game = ''.join(listUpper)
game = game.upper()
if len(sys.argv) == 2:
    if game.count('X')%2==0:
        move = 'X'
    else:
        move = 'O'
move = move.upper()

def printBoard(game):
    print('\n'.join([game[i*8:i*8+8] for i in range(8)]))

border = []
for i in range(8):
    border.append(i)
for i in range(8):
    border.append(i*8)
for i in range(8):
    border.append(i*8+7)
for i in range(8):
    border.append(56+i)

def returnValue(otherPos, iterator, current, game):
    i = current + iterator
    while i in otherPos:
        if i in border: return ''
        i += iterator
        if game[i] == '.':
            return i
    return ''

def legalMoves(game, move):
    if move=='X' or move == 'x':
        movePos = {i for i in range(64) if game[i]=='X'}
        otherPos = {i for i in range(64) if game[i]=='O'}
    else:
        movePos = {i for i in range(64) if game[i] == 'O'}
        otherPos = {i for i in range(64) if game[i] == 'X'}
    # otherMove = ['X','O','X'][['X','O','X'].index(move)+1]
    legal = set()
    for i in movePos:
        for j in otherPos:
            for x in [1, -1, -8, 8, -9, -7, 7, 9]:
                pos = returnValue(otherPos, x, i, game)
                if pos:
                    legal.add(pos)




                # if i+1==j and (j+1)%8 and game[j+1]=='.':           #right/left
            #     legal.add(j+1)
            # if i-1==j and (j-1)%8 and game[j-1]=='.':
            #     legal.add(j-1)
            #
            # if i+8==j and j+8<64 and game[j+8]=='.':                #up/down
            #     legal.add(j+8)
            # if i-8==j and j-8>0 and game[j-8]=='.':
            #     legal.add(j-8)
            #
            # if i+9==j and j+9<64 and game[j+9]=='.':                #diagonal
            #     legal.add(j+9)
            # if i+7==j and j+7<64 and game[j+7]=='.':
            #     legal.add(j+7)
            # if i-9==j and j-9>0 and game[j-9]=='.':
            #     legal.add(j-9)
            # if i-7==j and j-7>0 and game[j-7]=='.':
            #     legal.add(j-7)
    return legal

# printBoard(game)
# print('\n'*3)
# listgame = [*game]
# for i in legalMoves(game, move):
#     listgame[i] = 'A'
# printBoard(''.join(listgame))
if len(sys.argv) == 1:
    print(game)

start = time.time()
posMoves = legalMoves(game, move)
timeToRun = time.time()-start

if len(posMoves)>0: print('Possible moves:', legalMoves(game, move))
else: print('No moves are possible')