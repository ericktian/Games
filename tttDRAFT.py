import sys, time, msvcrt

### accepts no input, board is '.........', human player is X and goes first, press index for where u want to go




def printBoard(game):
    print('\n'.join([game[i*3:i*3+3] for i in range(3)]))

def whoseMove(game):
    return 'X' if game.count('X')==game.count('O') else 'O'

def freePositions(game):
    return {i for i in range(9) if game[i]=='.'}

threeInARow = [[0,1,2], [3,4,5], [6,7,8],
               [0,3,6], [1,4,7], [2,5,8],
               [0,4,8], [2,4,6]]

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

'##########'
def main(inp, game):
    # game = '.........'


    humanMove = int(inp)
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
        if moveInd != 'YOU LOSE!':
            listGame = [*game]
            listGame[int(moveInd)] = whoseMove(game)
            game = ''.join(listGame)
        else:
            ended = True
            print('')
    elif moveTup[2]:
        moveInd = moveTup[2].pop()
        if moveInd != 'TIE':
            listGame = [*game]
            listGame[int(moveInd)] = whoseMove(game)
            game = ''.join(listGame)
        else:
            ended = True
            print('')
    else:
        moveInd = moveTup[1].pop()
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

    return game

    #Steps: put in current game board and game will play best move for whoevers turn (X goes first)
    ### updated steps:
    ### put in no args, computer shows status of current game
    ### put in an index, that's your move
    ### put in "clear", the board becomes all empty again
'##########'




def gameOver(game):
    if '.' not in game: return True
    move = whoseMove(game)
    otherMove = ['X', 'O', 'X'][['X', 'O', 'X'].index(move) + 1]
    for j in range(8):
        if sum(game[i] == move for i in threeInARow[j]) == 3: return True
        if sum(game[i] == otherMove for i in threeInARow[j]) == 3: return True
    return False


def run(game):
    print('\n'*3)
    print('-----')
    print('Board:')
    printBoard(game)
    print('-----')
    print('')

    timeout = 5
    startTime = time.time()
    inp = None

    print('please make a move')
    #print("You have 5 seconds to make your move")
    while True:
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            break
        # elif time.time() - startTime > timeout:
        #     break

    if inp:
        if int(inp)<9 and game[int(inp)]=='.':
            print("Move configured...")
            newGame = main(inp, game)
            if not gameOver(newGame): run(newGame)
        else:
            print('\n'*3)
            print('Invalid move')
            run(game)
    else:
        print("You ran out of time")

# run('.........')

print(main('.........'))