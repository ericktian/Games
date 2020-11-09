# # # # # # # # # # # # temp = ['.']*64
# # # # # # # # # # # # temp[27] = 'X'
# # # # # # # # # # # # temp[28] = 'O'
# # # # # # # # # # # #
# # # # # # # # # # # # # temp[34] = 'O'
# # # # # # # # # # # # temp[35] = 'O'
# # # # # # # # # # # # temp[36] = 'O'
# # # # # # # # # # # # temp[44] = 'O'
# # # # # # # # # # # # print(''.join(temp))
# # # # # # # # # # # print('1'.upper())
# # # # # # # # # # # temp = [1, 3, 2]
# # # # # # # # # # # print([i for i in temp])
# # # # # # # # # # import time
# # # # # # # # # # print(time.time())
# # # # # # # # # # time.sleep(5)
# # # # # # # # # # print(time.time())
# # # # # # # # #
# # # # # # # # # # states = "AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY"
# # # # # # # # # # statesnew = states.split(" ")
# # # # # # # # # # toprt = ""
# # # # # # # # # # for i in range(len(statesnew)):
# # # # # # # # # #     toprt += "   " + str(i) + " " + statesnew[i]
# # # # # # # # # # print(toprt[:150]+"\n"+toprt[150:294]+"\n"+toprt[294:])
# # # # # # # # #
# # # # # # # # # temp = '''['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE',
# # # # # # # # # 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
# # # # # # # # # 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
# # # # # # # # # 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK',
# # # # # # # # # 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
# # # # # # # # # 'VA', 'WA', 'WV', 'WI', 'WY']'''
# # # # # # # # #
# # # # # # # # # print(''.join([i.lower() for i in temp]))
# # # # # # # #
# # # # # # # # corner = [0,7,56,63]
# # # # # # # # CorX = [[0,1,8,9], [7,6,14,15], [56,48,49,57], [63,54,55,62]]
# # # # # # # # edge = set()
# # # # # # # # for i in range(6):
# # # # # # # #    edge.add(i+1)
# # # # # # # #    edge.add(i+57)
# # # # # # # #    edge.add(8+i*8)
# # # # # # # #    edge.add(15+i*8)
# # # # # # # # borderTop = []
# # # # # # # # borderLeft = []
# # # # # # # # borderRight = []
# # # # # # # # borderBottom = []
# # # # # # # # for i in range(8): borderTop.append(i)
# # # # # # # # for i in range(8): borderLeft.append(i*8)
# # # # # # # # for i in range(8): borderRight.append(i*8+7)
# # # # # # # # for i in range(8): borderBottom.append(56+i)
# # # # # # # #
# # # # # # # # def wrapsAround(pos1, pos2):
# # # # # # # #    return pos1 in borderTop and pos2 in borderBottom or \
# # # # # # # #           pos1 in borderLeft and pos2 in borderRight or \
# # # # # # # #           pos1 in borderRight and pos2 in borderLeft or \
# # # # # # # #           pos1 in borderBottom and pos2 in borderTop
# # # # # # # # def connectedToCorner(index, game, move):
# # # # # # # #    if index not in edge: return False
# # # # # # # #    if move=='X': otherMove='O'
# # # # # # # #    else: otherMove='X'
# # # # # # # #    otherPos = {i for i in range(64) if game[i]==otherMove}
# # # # # # # #    for i in [-1,1,-8,8]:
# # # # # # # #        if wrapsAround(index, i): continue
# # # # # # # #        newInd = index+i
# # # # # # # #        while newInd in otherPos:
# # # # # # # #            if wrapsAround(newInd, i): break
# # # # # # # #            newInd+=i
# # # # # # # #            if newInd in corner and game[newInd]==move:
# # # # # # # #                return True
# # # # # # # #            if newInd>=0 and newInd<len(game) and game[newInd]==move:
# # # # # # # #                while newInd<len(game) and newInd>=0 and game[newInd]==move:
# # # # # # # #                    newInd+=i
# # # # # # # #                    if newInd in corner:
# # # # # # # #                        return True
# # # # # # # #    return False
# # # # # # # #
# # # # # # # # def CX(game, move):         ### returns bad moves for c or x
# # # # # # # #    toRet = set()
# # # # # # # #    for i in CorX:
# # # # # # # #        if game[i[0]]!=move:
# # # # # # # #            for j in i[1:]: toRet.add(j)
# # # # # # # #    return toRet
# # # # # # # #
# # # # # # # # def returnMove(posMoves, game, move):
# # # # # # # #    for i in posMoves:      			### checks for corners
# # # # # # # #        if i in corner:
# # # # # # # #            return i
# # # # # # # #    for i in posMoves:      			### checks for edge connected to corner
# # # # # # # #        if connectedToCorner(i, game, move):
# # # # # # # #            return i
# # # # # # # #    noCX = posMoves - CX(game, move)            ### avoids c or x moves
# # # # # # # #    if noCX: posMoves = noCX
# # # # # # # #    noEdge = posMoves - edge 			### avoids edge moves
# # # # # # # #    if noEdge: posMoves = noEdge
# # # # # # # #
# # # # # # # #    return posMoves.pop()
# # # # # # # #
# # # # # # #
# # # # # # # mv = 26
# # # # # # # mv1 = 11+(mv//8)*10+(mv%8)
# # # # # # # print(mv1)
# # # # # #
# # # # # # ### LAB 6 ###
# # # # # #
# # # # # # ### no random values and also checks if forms path from edge to corner
# # # # # #
# # # # # # #Othello is an 8*8 board with Xs, Os, and .s where . is an empty space
# # # # # # import sys, time, random
# # # # # # game = '...........................OX......XO...........................'
# # # # # # move = 'X'
# # # # # # if len(sys.argv) == 3:
# # # # # #     game = sys.argv[1]
# # # # # #     move = sys.argv[2]
# # # # # # elif len(sys.argv) == 2:
# # # # # #     game = sys.argv[1]
# # # # # #
# # # # # # game = game.upper().replace('@','X')
# # # # # # if len(sys.argv) == 2:
# # # # # #     if game.count('.')%2==0:
# # # # # #         move = 'X'
# # # # # #     else:
# # # # # #         move = 'O'
# # # # # # move = move.upper()
# # # # # #
# # # # # # # n = int(sys.argv[3])
# # # # # #
# # # # # # def printBoard(game):
# # # # # #     print('\n'.join([game[i*8:i*8+8] for i in range(8)]))
# # # # # #
# # # # # # borderTop = []
# # # # # # borderLeft = []
# # # # # # borderRight = []
# # # # # # borderBottom = []
# # # # # # for i in range(8): borderTop.append(i)
# # # # # # for i in range(8): borderLeft.append(i*8)
# # # # # # for i in range(8): borderRight.append(i*8+7)
# # # # # # for i in range(8): borderBottom.append(56+i)
# # # # # #
# # # # # # def wrapsAround(pos1, pos2):
# # # # # #     return pos1 in borderTop and pos2 in borderBottom or \
# # # # # #            pos1 in borderLeft and pos2 in borderRight or \
# # # # # #            pos1 in borderRight and pos2 in borderLeft or \
# # # # # #            pos1 in borderBottom and pos2 in borderTop
# # # # # #
# # # # # # def returnValue(otherPos, iterator, current, game):
# # # # # #     if wrapsAround(current, current+iterator): return ''
# # # # # #     i = current + iterator
# # # # # #     while i in otherPos:
# # # # # #         if wrapsAround(i, i+iterator): break
# # # # # #         i += iterator
# # # # # #
# # # # # #         if i<len(game) and i>=0 and game[i] == '.':
# # # # # #             return i
# # # # # #     return ''
# # # # # #
# # # # # # def legalMoves(game, move):
# # # # # #     if move=='X':
# # # # # #         movePos = {i for i in range(64) if game[i]=='X'}
# # # # # #         otherPos = {i for i in range(64) if game[i]=='O'}
# # # # # #     else:
# # # # # #         movePos = {i for i in range(64) if game[i] == 'O'}
# # # # # #         otherPos = {i for i in range(64) if game[i] == 'X'}
# # # # # #     legal = set()
# # # # # #     for i in movePos:
# # # # # #         for x in [1, -1, -8, 8, -9, -7, 7, 9]:
# # # # # #             pos = returnValue(otherPos, x, i, game)
# # # # # #             if pos != '':
# # # # # #                 legal.add(pos)
# # # # # #
# # # # # #     return legal
# # # # # #
# # # # # # ### lab 6 stuff ###
# # # # # # corner = [0,7,56,63]
# # # # # # CorX = [[0,1,8,9], [7,6,14,15], [56,48,49,57], [63,54,55,62]]        ### first ind = ind of corner
# # # # # # edge = set()
# # # # # # for i in range(6):
# # # # # #     edge.add(i+1)
# # # # # #     edge.add(i+57)
# # # # # #     edge.add(8+i*8)
# # # # # #     edge.add(15+i*8)
# # # # # # def connectedToCorner(index, game, move):
# # # # # #     if index not in edge: return False
# # # # # #     if move=='X': otherMove='O'
# # # # # #     else: otherMove='X'
# # # # # #     otherPos = {i for i in range(64) if game[i]==otherMove}
# # # # # #     for i in [-1,1,-8,8]:
# # # # # #         if wrapsAround(index, i): continue
# # # # # #         newInd = index+i
# # # # # #         while newInd in otherPos:
# # # # # #             if wrapsAround(newInd, i): break
# # # # # #             newInd+=i
# # # # # #             if newInd in corner and game[newInd]==move:
# # # # # #                 return True
# # # # # #             if newInd>=0 and newInd<len(game) and game[newInd]==move:
# # # # # #                 while newInd<len(game) and newInd>=0 and game[newInd]==move:
# # # # # #                     newInd+=i
# # # # # #                     if newInd in corner:
# # # # # #                         return True
# # # # # #     return False
# # # # # #
# # # # # # # def CorXbad(game, index, move):
# # # # # # #     for i in CorX:
# # # # # # #         if index in i and game[i[0]]!=move:         ### i know this checks the corners, but doesn't matter since they've already been checked
# # # # # # #             return True
# # # # # # #     return False
# # # # # #
# # # # # # def CX(game, move):         ### returns bad moves for c or x
# # # # # #     toRet = set()
# # # # # #     for i in CorX:
# # # # # #         if game[i[0]]!=move:
# # # # # #             for j in i[1:]: toRet.add(j)
# # # # # #     return toRet
# # # # # #
# # # # # # def returnMove(posMoves, game, move):
# # # # # #     for i in posMoves:      ### in corner
# # # # # #         if i in corner:
# # # # # #             return i
# # # # # #     for i in posMoves:      ### makes edge w corner
# # # # # #         if connectedToCorner(i, game, move):
# # # # # #             return i
# # # # # #     # for i in posMoves:      ### checks for indices not at C or X or an edge
# # # # # #     #     if not CorXbad(game, i, move) and i not in edge:
# # # # # #     #         return i
# # # # # #     # for i in posMoves:      ### checks for indices not at C or X
# # # # # #     #     if not CorXbad(game, i, move):
# # # # # #     #         return i
# # # # # #
# # # # # #     noCX = posMoves - CX(game, move)            ### only this can get to 73%
# # # # # #     if noCX: posMoves = noCX
# # # # # #     noEdge = posMoves - edge #########
# # # # # #     if noEdge: posMoves = noEdge
# # # # # #
# # # # # #     return posMoves.pop()
# # # # # #
# # # # # #
# # # # # # adjInds = [1, -1, -8, 8, -9, -7, 7, 9]
# # # # # # def resultBoard(game, token, move):
# # # # # #     toRet = list(game[:])
# # # # # #     toRet[move] = token
# # # # # #     otherToken = 'X' if token == 'O' else 'O'
# # # # # #     toBeFilled = []
# # # # # #     for i in adjInds:
# # # # # #         if wrapsAround(move, move + i): continue
# # # # # #         pos = move + i
# # # # # #         while pos < 64 and pos >= 0 and game[pos] == otherToken:
# # # # # #             if wrapsAround(pos, pos + i): break
# # # # # #             toBeFilled.append(pos)
# # # # # #             pos += i
# # # # # #             if pos < len(game) and pos >= 0 and game[pos] == token:
# # # # # #                 for i in toBeFilled:
# # # # # #                     toRet[i] = token
# # # # # #         toBeFilled = []
# # # # # #     return ''.join(toRet)
# # # # # #
# # # # # #
# # # # # # def evalBoard(board, token):
# # # # # #     otherToken = 'X' if token=='O' else 'O'
# # # # # #     myPoints = board.count(token)
# # # # # #     otherPoints = board.count(otherToken)
# # # # # #     #
# # # # # #     # for i in corner:                                    # Gives priority to corners
# # # # # #     #     if board[i]==token:
# # # # # #     #         myPoints+=500
# # # # # #     #     elif board[i]==otherToken:
# # # # # #     #         otherPoints+=500
# # # # # #     #
# # # # # #     # for i in edge:                                      # Gives priority to edges
# # # # # #     #                                                     # attached to corners
# # # # # #     #     if connectedToCorner(i, board, token):
# # # # # #     #         myPoints+=20
# # # # # #     #     elif connectedToCorner(i, board, otherToken):
# # # # # #     #         otherPoints+=20
# # # # # #     #     else:
# # # # # #     #         if board[i]==token: myPoints-=1             # Avoids edges otherwise
# # # # # #     #         else: otherPoints-=1
# # # # # #     #
# # # # # #     # myCX = CX(board, token)                         # Avoids positions C and X is
# # # # # #     #                                                 # corner is taken by other player
# # # # # #     # for i in myCX:
# # # # # #     #     if board[i]==token:
# # # # # #     #         myPoints-=1
# # # # # #     # otherCX = CX(board, token)
# # # # # #     # for i in otherCX:
# # # # # #     #     if board[i] == token:
# # # # # #     #         otherPoints-=1
# # # # # #
# # # # # #     return myPoints - otherPoints
# # # # # # def gameOver(board):
# # # # # #     if not legalMoves(board, 'X') and not legalMoves(board, 'O'): return True
# # # # # #     return False
# # # # # # def negamax(board, token, levels):
# # # # # #     if not levels: return [evalBoard(board, token)]
# # # # # #     if gameOver(board): return [evalBoard(board, token)]
# # # # # #
# # # # # #     lm = legalMoves(board, token)
# # # # # #     otherToken = 'X' if token == 'O' else 'O'
# # # # # #     if not lm:
# # # # # #         nm = negamax(board, otherToken, levels - 1) + [-1]
# # # # # #         return [-nm[0]] + nm[1:]
# # # # # #
# # # # # #     nmList = sorted([negamax(resultBoard(board, token, mv), otherToken, levels - 1) + [mv] for mv in lm])
# # # # # #     print(nmList)
# # # # # #     best = nmList[0]
# # # # # #     return [-best[0]] + best[1:]
# # # # # #
# # # # # #
# # # # # # # posMoves = legalMoves(game, move)
# # # # # # # print('Board:')
# # # # # # # printBoard(game)
# # # # # # # print('Possible Moves:', posMoves)
# # # # # # # if len(posMoves)>0: print('My heuristic choice is {}'.format(returnMove(posMoves,game,move)))
# # # # # #
# # # # # # ############################
# # # # # # n = 8
# # # # # # ############################
# # # # # #
# # # # # # if game.count('.') <= n:
# # # # # #     nm = negamax(game,move,-1)
# # # # # #     posMoves = legalMoves(game, move)
# # # # # #     print('Board:')
# # # # # #     printBoard(game)
# # # # # #     print('Possible Moves: ' + str(posMoves))
# # # # # #     print('My heuristic choice is {}'.format(returnMove(posMoves, game, move)))#returnMove(posMoves, game, move)))
# # # # # #     print('Negamax is running with n = ' + str(game.count('.')))
# # # # # #     print('Negamax returns', nm, 'and my move is', nm[-1])
# # # # # # else:
# # # # # #     posMoves = legalMoves(game, move)
# # # # # #     print('Board:')
# # # # # #     printBoard(game)
# # # # # #     print('Possible Moves:', posMoves)
# # # # # #     if len(posMoves)>0: print('My heuristic choice is {}'.format(returnMove(posMoves,game,move)))
# # # # #
# # # # # # strategy.py
# # # # # EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
# # # # #
# # # # #
# # # # # class Strategy():
# # # # #     def best_strategy(self, board, player, best_move, still_running):
# # # # #         level = 1
# # # # #         start = time.time()
# # # # #         while time.time() - start < 5:
# # # # #             brd = ''.join(board).replace('?', '').replace('@', 'X').replace('o', 'O')
# # # # #             move = 'X' if player == '@' else 'O'
# # # # #             mv = findBestMove(brd, move, level)
# # # # #             mv1 = 11 + (mv // 8) * 10 + (mv % 8)
# # # # #             best_move.value = mv1
# # # # #             level += 2
# # # # #
# # # # #
# # # # # import time, sys
# # # # #
# # # # #
# # # # #
# # # # #
# # # # # game = '...........................OX......XO...........................'
# # # # # move = 'X'
# # # # # if len(sys.argv) == 3:
# # # # #     game = sys.argv[1]
# # # # #     move = sys.argv[2]
# # # # # elif len(sys.argv) == 2:
# # # # #     game = sys.argv[1]
# # # # #
# # # # # game = game.upper()
# # # # # if len(sys.argv) == 2:
# # # # #     if game.count('.') % 2 == 0:
# # # # #         move = 'X'
# # # # #     else:
# # # # #         move = 'O'
# # # # # move = move.upper()
# # # # #
# # # # #
# # # # # def printBoard(game):
# # # # #     print('\n'.join([game[i * 8:i * 8 + 8] for i in range(8)]))
# # # # #
# # # # #
# # # # # game = '................................................................'
# # # # # listgame = list(game)
# # # # # for i in {3, 11, 15, 16, 19, 22, 25, 27, 29, 34, 35, 36, 40, 41, 42, 44, 45, 46, 47, 50, 51, 52, 57, 59, 61}:#{0, 7, 9, 15, 18, 23, 27, 31, 36, 39, 45, 47, 54, 55, 56, 57, 58, 59, 60, 61, 62}:#{6, 8, 14, 17, 22, 26, 30, 35, 38, 44, 46, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63}:#{1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 18, 24, 27, 32, 36, 40, 45, 48, 54, 56, 63}:
# # # # #     listgame[i] = 'A'
# # # # # printBoard(''.join(listgame))
# # # # # # exit()
# # # # #
# # # # #
# # # # # borderTop = []
# # # # # borderLeft = []
# # # # # borderRight = []
# # # # # borderBottom = []
# # # # # for i in range(8): borderTop.append(i)
# # # # # for i in range(8): borderLeft.append(i * 8)
# # # # # for i in range(8): borderRight.append(i * 8 + 7)
# # # # # for i in range(8): borderBottom.append(56 + i)
# # # # #
# # # # #
# # # # # def wrapsAround(pos1, pos2):
# # # # #     return pos1 in borderTop and pos2 in borderBottom or \
# # # # #            pos1 in borderLeft and pos2 in borderRight or \
# # # # #            pos1 in borderRight and pos2 in borderLeft or \
# # # # #            pos1 in borderBottom and pos2 in borderTop
# # # # #
# # # # #
# # # # # def returnValue(otherPos, iterator, current, game):
# # # # #     x = current + iterator
# # # # #     if wrapsAround(current, current + iterator) or (x >=len(game) or x<0): return ''
# # # # #     return current+iterator
# # # # #
# # # # #     i = current + iterator
# # # # #     while i in otherPos:
# # # # #         if wrapsAround(i, i + iterator): break
# # # # #         i += iterator
# # # # #
# # # # #         if i < len(game) and i >= 0 and game[i] == '.':
# # # # #             return i
# # # # #     return ''
# # # # #
# # # # #
# # # # # def legalMoves(game, move):
# # # # #     # if move == 'X':
# # # # #     #     movePos = {i for i in range(64) if game[i] == 'X'}
# # # # #     #     otherPos = {i for i in range(64) if game[i] == 'O'}
# # # # #     # else:
# # # # #     #     movePos = {i for i in range(64) if game[i] == 'O'}
# # # # #     #     otherPos = {i for i in range(64) if game[i] == 'X'}
# # # # #     otherPos = {}
# # # # #     legal = []
# # # # #     # for i in movePos:
# # # # #     for j in [1, -1, -8, 8, -9, -7, 7, 9]:
# # # # #         x = j
# # # # #         pos = returnValue(otherPos, x, move, game)
# # # # #         while pos != '':
# # # # #
# # # # #         # if pos != '':
# # # # #             legal.append(pos)
# # # # #             pos = returnValue(otherPos, x, pos, game)
# # # # #
# # # # #     return sorted(legal)
# # # # #
# # # # # look = [x for x in range(64)]
# # # # # for i in range(64):
# # # # #     look[i] = legalMoves(game, i)
# # # # #
# # # # # print(look)
# # # # # exit()
# # # # #
# # # # #
# # # # # ### lab 6 stuff ###
# # # # # corner = [0, 7, 56, 63]
# # # # # CorX = [[0, 1, 8, 9], [7, 6, 14, 15], [56, 48, 49, 57], [63, 54, 55, 62]]  ### first ind = ind of corner
# # # # # edge = set()
# # # # # for i in range(6):
# # # # #     edge.add(i + 1)
# # # # #     edge.add(i + 57)
# # # # #     edge.add(8 + i * 8)
# # # # #     edge.add(15 + i * 8)
# # # # #
# # # # #
# # # # # def connectedToCorner(index, game, move):
# # # # #     if index not in edge: return False
# # # # #     if move == 'X':
# # # # #         otherMove = 'O'
# # # # #     else:
# # # # #         otherMove = 'X'
# # # # #     otherPos = {i for i in range(64) if game[i] == otherMove}
# # # # #     for i in [-1, 1, -8, 8]:
# # # # #         if wrapsAround(index, i): continue
# # # # #         newInd = index + i
# # # # #         while newInd in otherPos:
# # # # #             if wrapsAround(newInd, i): break
# # # # #             newInd += i
# # # # #             if newInd in corner and game[newInd] == move:
# # # # #                 return True
# # # # #             if newInd >= 0 and newInd < len(game) and game[newInd] == move:
# # # # #                 while newInd < len(game) and newInd >= 0 and game[newInd] == move:
# # # # #                     newInd += i
# # # # #                     if newInd in corner:
# # # # #                         return True
# # # # #     return False
# # # # #
# # # # #
# # # # # def CX(game, move):  ### returns bad moves for c or x
# # # # #     toRet = set()
# # # # #     for i in CorX:
# # # # #         if game[i[0]] != move:
# # # # #             for j in i[1:]: toRet.add(j)
# # # # #     return toRet
# # # # #
# # # # #
# # # # # def returnMove(posMoves, game, move):
# # # # #     for i in posMoves:  ### in corner
# # # # #         if i in corner:
# # # # #             return i
# # # # #     for i in posMoves:  ### makes edge w corner
# # # # #         if connectedToCorner(i, game, move):
# # # # #             return i
# # # # #
# # # # #     noCX = posMoves - CX(game, move)  ### only this can get to 73%
# # # # #     if noCX: posMoves = noCX
# # # # #     noEdge = posMoves - edge  #########
# # # # #     if noEdge: posMoves = noEdge
# # # # #
# # # # #     return posMoves.pop()
# # # # #
# # # # #
# # # # # adjInds = [1, -1, -8, 8, -9, -7, 7, 9]
# # # # #
# # # # #
# # # # # def resultBoard(game, token, move):
# # # # #     toRet = list(game[:])
# # # # #     toRet[move] = token
# # # # #     otherToken = 'X' if token == 'O' else 'O'
# # # # #     toBeFilled = []
# # # # #     for i in adjInds:
# # # # #         if wrapsAround(move, move + i): continue
# # # # #         pos = move + i
# # # # #         while pos < 64 and pos >= 0 and game[pos] == otherToken:
# # # # #             if wrapsAround(pos, pos + i): break
# # # # #             toBeFilled.append(pos)
# # # # #             pos += i
# # # # #             if pos < len(game) and pos >= 0 and game[pos] == token:
# # # # #                 for i in toBeFilled:
# # # # #                     toRet[i] = token
# # # # #         toBeFilled = []
# # # # #     return ''.join(toRet)
# # # # #
# # # # #
# # # # # def evalBoard(board, token):
# # # # #     otherToken = 'X' if token == 'O' else 'O'
# # # # #     myPoints = board.count(token)
# # # # #     otherPoints = board.count(otherToken)
# # # # #     return myPoints - otherPoints
# # # # #
# # # # #
# # # # # def gameOver(board):
# # # # #     if not legalMoves(board, 'X') and not legalMoves(board, 'O'): return True
# # # # #     return False
# # # # #
# # # # #
# # # # # def negamax(board, token, levels):
# # # # #     if not levels: return [evalBoard(board, token)]
# # # # #     if gameOver(board): return [evalBoard(board, token)]
# # # # #
# # # # #     lm = legalMoves(board, token)
# # # # #     otherToken = 'X' if token == 'O' else 'O'
# # # # #     if not lm:
# # # # #         nm = negamax(board, otherToken, levels - 1) + [-1]
# # # # #         return [-nm[0]] + nm[1:]
# # # # #
# # # # #     nmList = sorted([negamax(resultBoard(board, token, mv), otherToken, levels - 1) + [mv] for mv in lm])
# # # # #     best = nmList[0]
# # # # #     return [-best[0]] + best[1:]
# # # # #
# # # # # def negamaxTerminal(brd, token ,improvable, hardBound):
# # # # #     enemy = 'X' if token == 'O' else 'O'
# # # # #     lm = legalMoves(brd, token)
# # # # #     if not lm:
# # # # #         lm = legalMoves(brd, enemy)
# # # # #         if not lm: return [evalBoard(brd, token)] ### game over
# # # # #         nm = negamaxTerminal(brd, enemy, -hardBound, -improvable) + [-1]
# # # # #         return [-nm[0]] + nm[1:]
# # # # #     best = []
# # # # #     newHB = -improvable
# # # # #     for mv in lm:
# # # # #         nm = negamaxTerminal(resultBoard(brd, token, mv), enemy, -hardBound, newHB) + [mv]
# # # # #         if not best or nm[0]<newHB:
# # # # #             best = nm
# # # # #             if nm[0]<newHB:
# # # # #                 newHB = nm[0]
# # # # #                 if -newHB>hardBound: return [-best[0]] + best[1:]
# # # # #     return [-best[0]] + best[1:]
# # # # #
# # # # # n = 10
# # # # #
# # # # #
# # # # # def findBestMove(game, move, level):
# # # # #     if game.count('.') <= n and level!=1:
# # # # #         nm = negamaxTerminal(game, move, -65, 65)
# # # # #         return nm[-1]  # returnMove(posMoves, game, move)))
# # # # #     else:
# # # # #         lm = legalMoves(game, move)
# # # # #         for i in lm:  ### in corner
# # # # #             if i in corner:
# # # # #                 return i
# # # # #         for i in lm:  ### makes edge w corner
# # # # #             if connectedToCorner(i, game, move):
# # # # #                 return i
# # # # #
# # # # #         nm = negamax(game, move, level)
# # # # #         return nm[-1]
# # # # #
# # # # #         # nm = negamax(game, move, level)
# # # # #         # return nm[-1]
# # # # #
# # # # #
# # # # # def main():
# # # # #     if game.count('.') <= n:
# # # # #         posMoves = legalMoves(game, move)
# # # # #         print('Board:')
# # # # #         printBoard(game)
# # # # #         print('Possible Moves: ' + str(posMoves))
# # # # #         print('My heuristic choice is {}'.format(returnMove(posMoves, game, move)))  # returnMove(posMoves, game, move)))
# # # # #         nm = negamaxTerminal(game, move, -65, 65)
# # # # #         print('Negamax is running with n = ' + str(game.count('.')))
# # # # #         print('Negamax returns', nm, 'and my move is', nm[-1])
# # # # #     else:
# # # # #         posMoves = legalMoves(game, move)
# # # # #         print('Board:')
# # # # #         printBoard(game)
# # # # #         print('Possible Moves:', posMoves)
# # # # #         if len(posMoves) > 0: print('My heuristic choice is {}'.format(returnMove(posMoves, game, move)))
# # # # #
# # # # #         for i in posMoves:  ### in corner
# # # # #             if i in corner:
# # # # #                 print(i)
# # # # #                 return
# # # # #         for i in posMoves:  ### makes edge w corner
# # # # #             if connectedToCorner(i, game, move):
# # # # #                 print(i)
# # # # #                 return
# # # # #         level = 3
# # # # #         start = time.time()
# # # # #         while time.time()-start < 5:
# # # # #             print(negamax(game, move, level)[-1])
# # # # #             level += 2
# # # # #
# # # # # if __name__ == "__main__":
# # # # #     main()
# # # # #
# # # # #
# # # # # # 13
# # # # # #### .XXXXXXX.OOOXOXX.OOXOXXXOOOXOOXXOOOOOXOX.OOOOOXX..OOOOOX......O. X
# # # # # #### ..OOOO.OXXOOOOOOXXXXOOXOXXXXXXOOXXXOXOOOXOXXOOOO..XXXX.X......X. O
# # # # #
# # # # # # 11
# # # # # # OOOOOOX..OOOOX.XXXOOXOX.XXXXXXOXXOXXXOO.XXXOXOOO..XXOOO...OOOO.O O
# # # # # # XXXXXXO.XXXOXOOXXOOXOOO.XXXOOXOOXXXXXXOXXOOOXOO.XOOOOO.OX....... X
# # # #
# # # # fullState = ["alabama","alaska","arizona","arkansas","california","colorado","connecticut","delaware",
# # # # "florida","georgia","hawaii","idaho","illinois","indiana","iowa","kansas","kentucky","louisiana","maine",
# # # # "maryland","massachusetts","michigan","minnesota","mississippi","missouri","montana","nebraska","nevada",
# # # # "new hampshire","new jersey","new mexico","new york","north carolina","north dakota","ohio","oklahoma",
# # # # "oregon","pennsylvania","rhode island","south carolina","south dakota","tennessee","texas","utah","vermont",
# # # # "virginia","washington","west virginia","wisconsin","wyoming"]
# # # #
# # # # abbState = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
# # # #             'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
# # # #             'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
# # # #             'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
# # # #
# # # # for i in range(len(abbState)):
# # # #     # print('var ' + '_'.join(fullState[i].split(' ')) + ' = document.getElementById(\'' + abbState[i] + '\');')
# # # #     # print('_'.join(fullState[i].split(' ')) + '.onClick = doClick(' + '_'.join(fullState[i].split(' ')) + ');')
# # # #     print('if(' + '_'.join(fullState[i].split(' ')) + '==')
# # # # #     abbState[i] = abbState[i].upper()
# # # # # print(abbState)
# # #
# # # # strategy.py
# # # EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
# # #
# # #
# # # class Strategy():
# # #     def best_strategy(self, board, player, best_move, still_running):
# # #         level = 1
# # #         start = time.time()
# # #         while time.time() - start < 5:
# # #             brd = ''.join(board).replace('?', '').replace('@', 'X').replace('o', 'O')
# # #             move = 'X' if player == '@' else 'O'
# # #             mv = findBestMove(brd, move, level)
# # #             mv1 = 11 + (mv // 8) * 10 + (mv % 8)
# # #             best_move.value = mv1
# # #             level += 2
# # #
# # #
# # # import time, sys
# # #
# # # game = '...........................OX......XO...........................'
# # # move = 'X'
# # # if len(sys.argv) == 3:
# # #     game = sys.argv[1]
# # #     move = sys.argv[2]
# # # elif len(sys.argv) == 2:
# # #     game = sys.argv[1]
# # #
# # # game = game.upper()
# # # if len(sys.argv) == 2:
# # #     if game.count('.') % 2 == 0:
# # #         move = 'X'
# # #     else:
# # #         move = 'O'
# # # move = move.upper()
# # #
# # #
# # # def printBoard(game):
# # #     print('\n'.join([game[i * 8:i * 8 + 8] for i in range(8)]))
# # #
# # #
# # # borderTop = []
# # # borderLeft = []
# # # borderRight = []
# # # borderBottom = []
# # # for i in range(8): borderTop.append(i)
# # # for i in range(8): borderLeft.append(i * 8)
# # # for i in range(8): borderRight.append(i * 8 + 7)
# # # for i in range(8): borderBottom.append(56 + i)
# # #
# # #
# # # def debugBoard(game, moves):
# # #     listgame = list(game)
# # #     for i in moves:
# # #         listgame[i] = '*'
# # #     return ''.join(listgame)
# # #
# # #
# # # def wrapsAround(pos1, pos2):
# # #     return pos1 in borderTop and pos2 in borderBottom or \
# # #            pos1 in borderLeft and pos2 in borderRight or \
# # #            pos1 in borderRight and pos2 in borderLeft or \
# # #            pos1 in borderBottom and pos2 in borderTop
# # #
# # #
# # # # def returnValue(otherPos, iterator, current, game):
# # # #     if wrapsAround(current, current + iterator): return ''
# # # #     i = current + iterator
# # # #     while i in otherPos:
# # # #         if wrapsAround(i, i + iterator): break
# # # #         i += iterator
# # # #
# # # #         if i < len(game) and i >= 0 and game[i] == '.':
# # # #             return i
# # # #     return ''
# # #
# # # adjInds = [1, -1, -8, 8, -9, -7, 7, 9]
# # #
# # # def legalMoves(game, move):
# # #     otherMove = 'X' if move == 'O' else 'O'
# # #     movePos = {i for i in range(64) if game[i] == move}
# # #     otherPos = {i for i in range(64) if game[i] == otherMove}
# # #     legal = {}
# # #     for i in movePos:
# # #         for x in adjInds:
# # #             pos = ''
# # #
# # #             toBeFilled = set()
# # #             if not wrapsAround(i, i + x):
# # #                 current = i + x
# # #                 while current in otherPos:
# # #                     toBeFilled.add(current)
# # #
# # #                     if wrapsAround(current, current + x) or current+x>=len(game) or current+x<0:
# # #                         break
# # #                     if game[current+x] == '.':
# # #                         pos = current+x
# # #                     current += x
# # #
# # #             if pos:
# # #                 legal[pos] = toBeFilled
# # #
# # #     return legal
# # #
# # # # def resultBoard(game, token, move, lm):#game, token, move):
# # # #     otherMove = 'X' if token == 'O' else 'O'
# # # #     toRet = list(game)                                  ###
# # # #     for i in lm[move]:
# # # #         toRet[i] = otherMove
# # # #     return ''.join(toRet)
# # # def resultBoard(game, token, move, lm):
# # #    toRet = list(game[:])
# # #    toRet[move] = token
# # #    otherToken = 'X' if token == 'O' else 'O'
# # #    toBeFilled = []
# # #    for i in adjInds:
# # #        if wrapsAround(move, move + i): continue
# # #        pos = move + i
# # #        while pos < 64 and pos >= 0 and game[pos] == otherToken:
# # #            if wrapsAround(pos, pos + i): break
# # #            toBeFilled.append(pos)
# # #            pos += i
# # #            if pos < len(game) and pos >= 0 and game[pos] == token:
# # #                for i in toBeFilled:
# # #                    toRet[i] = token
# # #        toBeFilled = []
# # #    return ''.join(toRet)
# # #
# # #
# # #
# # # ### lab 6 stuff ###
# # # corner = [0, 7, 56, 63]
# # # CorX = [[0, 1, 8, 9], [7, 6, 14, 15], [56, 48, 49, 57], [63, 54, 55, 62]]  ### first ind = ind of corner
# # # edge = set()
# # # for i in range(6):
# # #     edge.add(i + 1)
# # #     edge.add(i + 57)
# # #     edge.add(8 + i * 8)
# # #     edge.add(15 + i * 8)
# # #
# # #
# # # def connectedToCorner(index, game, move):
# # #     if index not in edge: return False
# # #     if move == 'X':
# # #         otherMove = 'O'
# # #     else:
# # #         otherMove = 'X'
# # #     otherPos = {i for i in range(64) if game[i] == otherMove}
# # #     for i in [-1, 1, -8, 8]:
# # #         if wrapsAround(index, i): continue
# # #         newInd = index + i
# # #         while newInd in otherPos:
# # #             if wrapsAround(newInd, i): break
# # #             newInd += i
# # #             if newInd in corner and game[newInd] == move:
# # #                 return True
# # #             if newInd >= 0 and newInd < len(game) and game[newInd] == move:
# # #                 while newInd < len(game) and newInd >= 0 and game[newInd] == move:
# # #                     newInd += i
# # #                     if newInd in corner:
# # #                         return True
# # #     return False
# # #
# # #
# # # def CX(game, move):  ### returns bad moves for c or x
# # #     toRet = set()
# # #     for i in CorX:
# # #         if game[i[0]] != move:
# # #             for j in i[1:]: toRet.add(j)
# # #     return toRet
# # #
# # #
# # # def returnMove(posMoves, game, move):
# # #     for i in posMoves:  ### in corner
# # #         if i in corner:
# # #             return i
# # #     for i in posMoves:  ### makes edge w corner
# # #         if connectedToCorner(i, game, move):
# # #             return i
# # #
# # #     noCX = posMoves - CX(game, move)  ### only this can get to 73%
# # #     if noCX: posMoves = noCX
# # #     noEdge = posMoves - edge  #########
# # #     if noEdge: posMoves = noEdge
# # #
# # #     return posMoves.pop()
# # #
# # #
# # #
# # # def evalBoard(board, token):
# # #     otherToken = 'X' if token == 'O' else 'O'
# # #     myPoints = board.count(token)
# # #     otherPoints = board.count(otherToken)
# # #     return myPoints - otherPoints
# # #
# # #
# # # def gameOver(board):
# # #     if not legalMoves(board, 'X') and not legalMoves(board, 'O'): return True
# # #     return False
# # #
# # #
# # # def negamax(board, token, levels):
# # #     if not levels: return [evalBoard(board, token)]
# # #     if gameOver(board): return [evalBoard(board, token)]
# # #
# # #     lm = legalMoves(board, token)
# # #     otherToken = 'X' if token == 'O' else 'O'
# # #     if not lm:
# # #         nm = negamax(board, otherToken, levels - 1) + [-1]
# # #         return [-nm[0]] + nm[1:]
# # #
# # #     nmList = sorted([negamax(resultBoard(board, token, mv, lm), otherToken, levels - 1) + [mv] for mv in lm])
# # #     best = nmList[0]
# # #     return [-best[0]] + best[1:]
# # #
# # # def negamaxTerminal(brd, token ,improvable, hardBound):
# # #     enemy = 'X' if token == 'O' else 'O'
# # #     lm = legalMoves(brd, token)
# # #     if not lm:
# # #         lm = legalMoves(brd, enemy)
# # #         if not lm: return [evalBoard(brd, token)] ### game over
# # #         nm = negamaxTerminal(brd, enemy, -hardBound, -improvable) + [-1]
# # #         return [-nm[0]] + nm[1:]
# # #     best = []
# # #     newHB = -improvable
# # #     for mv in lm:
# # #         nm = negamaxTerminal(resultBoard(brd, token, mv, lm), enemy, -hardBound, newHB) + [mv]
# # #         if not best or nm[0]<newHB:
# # #             best = nm
# # #             if nm[0]<newHB:
# # #                 newHB = nm[0]
# # #                 if -newHB>hardBound: return [-best[0]] + best[1:]
# # #     return [-best[0]] + best[1:]
# # #
# # # n = 15
# # #
# # #
# # # def findBestMove(game, move, level):
# # #     if game.count('.') <= n and level!=1:
# # #         nm = negamaxTerminal(game, move, -65, 65)
# # #         return nm[-1]  # returnMove(posMoves, game, move)))
# # #     else:
# # #         lm = legalMoves(game, move)
# # #         for i in lm:  ### in corner
# # #             if i in corner:
# # #                 return i
# # #         for i in lm:  ### makes edge w corner
# # #             if connectedToCorner(i, game, move):
# # #                 return i
# # #
# # #         nm = negamax(game, move, level)
# # #         return nm[-1]
# # #
# # #         # nm = negamax(game, move, level)
# # #         # return nm[-1]
# # #
# # #
# # # def main():
# # #     if game.count('.') <= n:
# # #         posMoves = set(legalMoves(game, move))
# # #         print('Board:')
# # #         printBoard(game)
# # #         print('Possible Moves: ' + str(posMoves))
# # #         print('My heuristic choice is {}'.format(returnMove(posMoves, game, move)))  # returnMove(posMoves, game, move)))
# # #         nm = negamaxTerminal(game, move, -65, 65)
# # #         print('Negamax is running with n = ' + str(game.count('.')))
# # #         print('Negamax returns', nm, 'and my move is', nm[-1])
# # #     else:
# # #         posMoves = set(legalMoves(game, move))
# # #         print('Board:')
# # #         printBoard(game)
# # #         print('Possible Moves:', posMoves)
# # #         if len(posMoves) > 0: print('My heuristic choice is {}'.format(returnMove(posMoves, game, move)))
# # #
# # # if __name__ == "__main__":
# # #     main()
# #
# # # abbState = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de',
# # # 'fl', 'ga', 'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me',
# # # 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv',
# # # 'nh', 'nj', 'nm', 'ny', 'nc', 'nd', 'oh', 'ok',
# # # 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt',
# # # 'va', 'wa', 'wv', 'wi', 'wy']
# # #
# # # abb2 = [x for x in range(50)]
# # # for i in range(len(abbState)):
# # #     abb2[i] = abbState[i].upper()
# # #
# # # print(abb2)
# #
# # fullState = ["alabama","alaska","arizona","arkansas","california","colorado","connecticut","delaware",
# # "florida","georgia","hawaii","idaho","illinois","indiana","iowa","kansas","kentucky","louisiana","maine",
# # "maryland","massachusetts","michigan","minnesota","mississippi","missouri","montana","nebraska","nevada",
# # "new hampshire","new jersey","new mexico","new york","north carolina","north dakota","ohio","oklahoma",
# # "oregon","pennsylvania","rhode island","south carolina","south dakota","tennessee","texas","utah","vermont",
# # "virginia","washington","west virginia","wisconsin","wyoming"]
# # # for i in fullState:
# # #     print("<li><a href=\"javascript:void(0)\">" + i[0].upper() + i[1:] + "</a></li>")
# # fullState2 = []
# # for i in fullState:
# #     fullState2.append(i.upper())
# # print(fullState2)
#
# # infile = open("wordss.txt", "r")
# fullState = ["alabama","alaska","arizona","arkansas","california","colorado","connecticut","delaware",
# "florida","georgia","hawaii","idaho","illinois","indiana","iowa","kansas","kentucky","louisiana","maine",
# "maryland","massachusetts","michigan","minnesota","mississippi","missouri","montana","nebraska","nevada",
# "new hampshire","new jersey","new mexico","new york","north carolina","north dakota","ohio","oklahoma",
# "oregon","pennsylvania","rhode island","south carolina","south dakota","tennessee","texas","utah","vermont",
# "virginia","washington","west virginia","wisconsin","wyoming"]
# fs = [x for x in range(len(fullState))]
# for i in range(len(fullState)):
#     fs[i] = fullState[i].upper()
# print(fs)
fullState = ['ALABAMA', 'ALASKA', 'ARIZONA', 'ARKANSAS', 'CALIFORNIA', 'COLORADO', 'CONNECTICUT', 'DELAWARE', 'FLORIDA',
'GEORGIA', 'HAWAII', 'IDAHO', 'ILLINOIS', 'INDIANA', 'IOWA', 'KANSAS', 'KENTUCKY', 'LOUISIANA', 'MAINE', 'MARYLAND',
'MASSACHUSETTS', 'MICHIGAN', 'MINNESOTA', 'MISSISSIPPI', 'MISSOURI', 'MONTANA', 'NEBRASKA', 'NEVADA', 'NEW HAMPSHIRE',
'NEW JERSEY', 'NEW MEXICO', 'NEW YORK', 'NORTH CAROLINA', 'NORTH DAKOTA', 'OHIO', 'OKLAHOMA', 'OREGON', 'PENNSYLVANIA',
'RHODE ISLAND', 'SOUTH CAROLINA', 'SOUTH DAKOTA', 'TENNESSEE', 'TEXAS', 'UTAH', 'VERMONT', 'VIRGINIA', 'WASHINGTON',
'WEST VIRGINIA', 'WISCONSIN', 'WYOMING']
fs = []
for i in fullState:
    fs.append(i[0]+i[1:].lower())
print(fs)