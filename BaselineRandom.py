#
# BaselineRandom.py by Peter Gabor
# for Othello testing purposes
# 2 Feb 2016
#
import sys, time, math, random

# Debugging info
from os import path
import re

# pyver = re.sub(' [^Z]*', "", sys.version)
# print ("Python version {} running {}".format(pyver, path.basename(__file__)))


# If a board is given, determine the symbol for a blank
if len(sys.argv) > 1:
    board = sys.argv[1].upper()
    for theBlank in board:
        if theBlank != "X" and theBlank != "O": break
    if theBlank == "X" or theBlank == "O":
        print("Game is already over")
        exit()
else:
    # Otherwise assume a standard starting position
    theBlank = "."
    board = (theBlank * (3 * 8 + 3)) + "OX" + theBlank * 6 + "XO" + (theBlank * (3 * 8 + 3))

# If no token is given, assume no Passes have happened and deduce it
token = sys.argv[2].upper() if len(sys.argv) > 2 else ("O" if board.count(theBlank) % 2 else "X")


def defineNeighbors(bL):
    # bL = the board length
    b2 = bL * bL

    aNeigh = [{p + 1, p - 1, p + bL, p - bL, p + bL - 1, p + bL + 1, p - bL - 1, p - bL + 1} for p in range(b2)]

    # Adjust edges:
    for p in range(0, bL): aNeigh[p] -= {p - bL - 1, p - bL, p - bL + 1}
    for p in range(0, b2, bL): aNeigh[p] -= {p - 1, p - bL - 1, p + bL - 1}
    for p in range(bL - 1, b2, bL): aNeigh[p] -= {p + 1, p + bL + 1, p - bL + 1}
    for p in range(b2 - bL, b2): aNeigh[p] -= {p + bL - 1, p + bL, p + bL + 1}

    # Adjust corners (should be redundant):
    aNeigh[0] = {1, bL, bL + 1}
    aNeigh[bL - 1] = {bL - 2, 2 * bL - 1, 2 * bL - 2}
    aNeigh[b2 - 1] = {b2 - 2, b2 - bL - 1, b2 - bL - 2}
    aNeigh[b2 - bL] = {b2 - bL + 1, b2 - 2 * bL, b2 - 2 * bL + 1}

    return aNeigh


def findMoves(board, token, aNeigh):
    b2 = len(board)
    enemy = "X" if token == "O" else "O"
    setMoves = set()
    for p in range(b2):
        if board[p] != theBlank: continue
        moveFound = False
        for np in aNeigh[p]:
            if board[np] != enemy: continue
            diff = np - p
            while np + diff in aNeigh[np]:
                np += diff
                if board[np] != enemy:
                    moveFound = (board[np] == token)
                    break
            if moveFound:
                setMoves.add(p)
                break
    return setMoves


aNeigh = defineNeighbors(int(math.sqrt(len(board))))

setMoves = findMoves(board, token, aNeigh)

if len(setMoves) == 0: print("P"); exit()
print("{}".format(random.sample(list(setMoves), 1)[0]))

