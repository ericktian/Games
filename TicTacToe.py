#game is 3x3 of Xs, Os, and .s where . is empty
#input = board, and the computer responds w the board w their move
import sys

#METHODS

#1
def printBoard(game):
    print('\n'.join([game[i*3:i*3+3] for i in range(3)]))

#2
def whoseMove(game):
    return 'X' if game.count('X')==game.count('O') else 'O'

#3
def freePositions(game):
    return {i for i in range(9) if game[i]=='.'}


#lookup
threeInARow = [[0,1,2], [3,4,5], [6,7,8],
               [0,3,6], [1,4,7], [2,5,8],
               [0,4,8], [2,4,6]]
#partitionMoves
def partitionMoves(game):
    move = whoseMove(game)
    otherMove = ['X','O','X'][['X','O','X'].index(move)+1]
    for j in range(8):                              #if move has a 3 in a row, we win, if otherMove has 3 in a row, we lose
        if sum(game[i]==move for i in threeInARow[j]) == 3: return {'YOU LOSE!'},{},{}
        if sum(game[i]==otherMove for i in threeInARow[j]) == 3: return {},{'YOU WIN!'},{}
    if '.' not in game: return {},{},{'TIE'}           #if game is a tie

    good,bad,tie = set(),set(),set()
    for i in freePositions(game):
        listGame = [*game]
        listGame[i] = whoseMove(game)
        newGame = ''.join(listGame)
        tempGood,tempBad,tempTie = partitionMoves(newGame)
        if tempGood: bad.add(i)
        elif tempTie: tie.add(i)
        else: good.add(i)
    return good,bad,tie



#MAIN
# printBoard(game)
# print('Move:', whoseMove(game))
# print('Empty Positions:', freePositions(game))
# print('partitionMoves:', partitionMoves(game))


# humanMove = ''
# if len(sys.argv)>1: humanMove = sys.argv[1]
# else: humanMove = 'X'
# board = ''
# if len(sys.argv)>2: board = sys.argv[2]
# else: board = '.........'

#game = sys.argv[1]                 ###board is now saved to a .txt file
infile = open('board.txt', 'r')
game = infile.readline()

### if no arguments, print current board
if len(sys.argv)==1:
    print('Board:')
    printBoard(game)
    exit()

### clear board
if sys.argv[1]=='clear':
    infile.close()
    outfile = open('board.txt', 'w')
    outfile.write('.'*9)
    outfile.close()
    exit()

humanMove = int(sys.argv[1])
move = whoseMove(game)
listGame = [*game]
listGame[humanMove] = move
game = ''.join(listGame)
print('Your move:', humanMove)                 ### your move shows
printBoard(game)
print('')

ended = False
moveTup = partitionMoves(game)
if moveTup[0]:
    moveInd = moveTup[0].pop()
    # print('Move:', moveInd)
    if moveInd != 'YOU LOSE!':
        listGame = [*game]
        listGame[int(moveInd)] = whoseMove(game)
        game = ''.join(listGame)
    else:
        ended = True
        print('')
elif moveTup[2]:
    moveInd = moveTup[2].pop()
    # print('Move:', moveInd)
    if moveInd != 'TIE':
        listGame = [*game]
        listGame[int(moveInd)] = whoseMove(game)
        game = ''.join(listGame)
    else:
        ended = True
        print('')
else:
    moveInd = moveTup[1].pop()
    # print('Move:', moveInd)
    if moveInd != 'YOU WIN!':
        listGame = [*game]
        listGame[int(moveInd)] = whoseMove(game)
        game = ''.join(listGame)
    else:
        ended = True
        print('')
move = whoseMove(game)
otherMove = ['X','O','X'][['X','O','X'].index(move)+1]
for j in range(8):                              #if move has a 3 in a row, we win, if otherMove has 3 in a row, we lose
    if sum(game[i]==move for i in threeInARow[j]) == 3: print('YOU WIN')
    if sum(game[i]==otherMove for i in threeInARow[j]) == 3: print('YOU LOSE')
if '.' not in game: print('TIE')           #if game is a tie

if not ended:
    print('Computer move:', moveInd)                 ### Computer's move shows
    printBoard(game)

infile.close()
outfile = open('board.txt', 'w')
outfile.write(game)

#Steps: put in current game board and game will play best move for whoevers turn (X goes first)
### updated steps:
### put in no args, computer shows status of current game
### put in an index, that's your move
### put in "clear", the board becomes all empty again