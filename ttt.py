import sys, time, msvcrt
### METHODS
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
    for j in range(8):
        if sum(game[i]==move for i in threeInARow[j]) == 3: return {'YOU LOSE!'},{},{}      ### loss
        if sum(game[i]==otherMove for i in threeInARow[j]) == 3: return {},{'YOU WIN!'},{}  ### win
    if '.' not in game: return {},{},{'TIE'}                                                ### tie

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

def main(inp, game):
    humanMove = ''
    humanSign = ''
    if inp != 'cpu':                                    ### if computer moves first
        humanMove = int(inp)
        move = whoseMove(game)
        humanSign = move
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

    if inp != 'cpu':
        if partitionMoves(game)[1] == {'YOU WIN!'}:
            if move != humanSign: print('YOU WIN!')
            else: print('YOU LOSE!')
        # otherMove = ['X','O','X'][['X','O','X'].index(move)+1]
        # for j in range(8):                                                              ### determine if game is over
        #     if sum(game[i]==move for i in threeInARow[j]) == 3:
        #         if inp != 'cpu': print('YOU WIN')
        #     if sum(game[i]==otherMove for i in threeInARow[j]) == 3:
        #         if inp != 'cpu': print('YOU LOSE')
        if '.' not in game: print('TIE')

    if not ended:
        print('Computer move:', moveInd)                 ### Computer's move shows
        printBoard(game)

    return game





def gameOver(game, move, firstorsecond):
    if '.' not in game: return 'YOU TIE'
    otherMove = ['X', 'O', 'X'][['X', 'O', 'X'].index(move) + 1]
    for j in range(8):
        if sum(game[i] == move for i in threeInARow[j]) == 3:
            if firstorsecond == 1: return 'YOU WIN!'
            else: return 'YOU LOSE!'
        elif sum(game[i] == otherMove for i in threeInARow[j]) == 3:
            if firstorsecond == 1: return 'YOU LOSE!'
            else: return 'YOU WIN!'
    return ''


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

    print('Make a move!')
    while True:
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            break

    if inp:
        if int(inp)<9 and game[int(inp)]=='.':
            print('')
            newGame = main(inp, game)
            if not gameOver(newGame, 'X', 1): run(newGame)
        else:
            print('\n'*3)
            print('Invalid move')
            run(game)

if len(sys.argv) == 1:
    print('Computer move:', 0)
    run('X........')
elif len(sys.argv) == 2:
    input = sys.argv[1]
    if len(input) > 1:
        inputBoard = main('cpu', input)
        if gameOver(inputBoard, whoseMove(input), 0):
            print('')
            printBoard(inputBoard)
            print(gameOver(inputBoard, whoseMove(input), 0))
        else:
            run(inputBoard)
    else:
        if input == 'X':
            run('.........')
        elif input == 'O':
            run('X........')
        else:
            print('invalid, you must input must be in the format [board] [player move]')
elif len(sys.argv) == 3:
    input1 = sys.argv[1]
    input2 = sys.argv[2]
    whoToMove = whoseMove(input1)
    if input2 == whoToMove:
        # print('here')
        if gameOver(input1, input2, 1):
            print('')
            printBoard(input1)
            print(gameOver(input1, input2, 1))
        else:
            run(input1)
    else:
        # print('here1')
        inputBoard = main('cpu', input1)
        if gameOver(inputBoard, input2, 1):
            print('')
            printBoard(inputBoard)
            print(gameOver(inputBoard, input2, 1))
        else:
            run(inputBoard)