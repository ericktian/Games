#game is 3x3 of Xs, Os, and .s where . is empty
import sys
game = sys.argv[1]

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
        if sum(game[i]==move for i in threeInARow[j]) == 3: return {''},{},{}
        if sum(game[i]==otherMove for i in threeInARow[j]) == 3: return {},{''},{}
    if '.' not in game: return {},{},{''}           #if game is a tie

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
printBoard(game)
print('Move:', whoseMove(game))
print('Empty Positions:', freePositions(game))
print('partitionMoves:', partitionMoves(game))