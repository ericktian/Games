# Arya Kumar, Jan 31st 2018
# Othello Lab A Manager (portions of code copied from Dr. Gabor's manager.py)

### IMPORTS ###
import sys, os, re, multiprocessing
from random import choice
from subprocess import Popen, TimeoutExpired, PIPE

### VARS ###
directions = {(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)}
playerNames = []
secondsPerMove = 5
numGames = 1

### GET ARGS ###
fileSpecs = []
for arg in sys.argv[1:]:
	try:
		numGames = int(arg)
	except ValueError:
		fileSpecs.append(arg)

### GET THE FILES THEMSELVES ###
def findFile(fs):
	if fs == "random": return {fs} # Hardcoded baseline random
	mypath = os.getcwd()
	if fs[-3:]==".py":               # If explicit filename is provided, then we must mean that one without capitalization
		if os.path.isfile(fs): return {fs}
		else: exit("File not found: {}".format(fs))
	else:                            # If unique prefix is provided
		fs = fs.lower()
		for _, _, filenames in os.walk(mypath):
			setOfScripts = {*filenames}  # Gets all files in the path
			break
		setOfScripts = {s for s in setOfScripts if s[:len(fs)].lower()==fs and s[-3:]==".py"}
	return setOfScripts if len(setOfScripts)==1 else exit("File spec is not unique!")

if not fileSpecs: exit("No primary filename provided!") # No primary file given
if len(fileSpecs) == 1: fileSpecs.append("random") # No secondary file needed
playerNames = tuple(findFile(f).pop() for f in fileSpecs)

### BOARD MANIPULATIONS ###
def isValidPos(r, c):
	""" Returns whether a move is a valid position """
	return 0 <= r < 8 and 0 <= c < 8

def opponent(token):
	""" Returns the opposite of a given token """
	return "O" if token == "X" else "X"

def validMoves(board, token):
	""" Given a board and a token, finds all the valid moves """
	opponentToken = opponent(token)

	def checkDirection(R, C, dr, dc):
		r, c = R+dr, C+dc # Save original position
		while isValidPos(r, c) and board[r*8+c] == opponentToken:
			r, c = r+dr, c+dc
		return isValidPos(r, c) and board[r*8+c] == token and (abs(R-r) > 1 or abs(C-c) > 1)

	return {R*8+C for dr, dc in directions for R, C in (divmod(k, 8) for k in range(64) if board[k] == ".") if checkDirection(R, C, dr, dc)}

def makeMove(board, token, move):
	(R, C), opponentToken = divmod(move, 8), opponent(token)

	def checkDirection(dr, dc):
		tempflips, r, c = set(), R+dr, C+dc
		while isValidPos(r, c) and board[r*8+c] == opponentToken:
			tempflips.add(r*8+c)
			r, c = r+dr, c+dc
		return tempflips if isValidPos(r, c) and board[r*8+c] == token and (abs(R-r) > 1 or abs(C-c) > 1) else set()

	flips = {move}.union(*(checkDirection(dr, dc) for dr, dc in directions))
	return ''.join(v if k not in flips else token for k, v in enumerate(board))

### GAME RUNNING FUNCTIONS ###

# Regular Expressions:
rexSyn1     = re.compile(", line (\\d+)$\\s*^\\s*(.*?)$.*SyntaxError:", re.S | re.M)
rexScript   = re.compile("^Traceback.*line (\\d+).*^\\s*(.+)$.*^(.+)$", re.M | re.S)
rexDecimals = re.compile("\\d+[.]\\d*|[.]\\d+")
rexLastNum  = re.compile("(\\d+)\\D*$")

def getMove(player, board, token, n):
	# Runs command as separate thread in case it takes too long :)
	if player == "random": # Hardcoded baseline random
		return choice(list(validMoves(board, token)))

	# Threaded player:
	timedOut, proc = False, Popen([ sys.executable , "-u", player , board, token, str(n)], stdout=PIPE, stderr=PIPE)
	try:
		actualOut, errOut = proc.communicate(timeout=secondsPerMove)
	except TimeoutExpired:
		timedOut = True
		proc.kill()
		actualOut, errOut = proc.communicate()
	actualOut, errOut = actualOut.decode(), errOut.decode()

	grps = rexSyn1.search(errOut)
	if grps: exit("Syntax error on line {}: {}".format(grps.group(1), grps.group(2)))

	if errOut and not timedOut:
		grps = rexScript.search(errOut)
		if grps: exit("Script error at line {}: {}\n  {}".format(grps.group(1), grps.group(2), grps.group(3)))
		return exit("Unknown error:\n{}".format(errOut))

	if timedOut: return -1

	grps = rexLastNum.search(rexDecimals.sub("", actualOut))
	if not grps: exit(errOut + ("/ " if errOut else "") + "No move given")
	return int(grps.group(1))

def runGame(p1, p2, n):
	""" Runs a single game, returning {"random":1, "labA.py":63} """
	board, token = "." * 27 + "OX......XO" + "." * 27, "O"
	tokenPlayers = {"O":p1, "X":p2}
	while board.count(".") and (validMoves(board, "X") or validMoves(board, "O")):
		vms = validMoves(board, token)
		if not vms: # No valid moves: Switch sides
			token = opponent(token)
			vms = validMoves(board, token)
		mv = getMove(tokenPlayers[token], board, token, n) # Get the move
		if mv not in vms:
			return {p1:0, p2:0}
		board = makeMove(board, token, mv) # Make the move
		token = opponent(token) # flip
	return {p1:board.count("O"), p2:board.count("X")} # Return counts

### FIRST GRAPH - Average Capture Rate vs N ###
results, counter = [], 0
class BreakoutException(Exception): pass
gnu = """ set terminal png size 650,900
set datafile separator comma
set output "graph.png"
set title "Average Capture Rate ({} games) vs Negamax Depth"
set boxwidth 1
set style fill solid border lt -1
set xlabel "Negamax Depth"
set ylabel "Average Capture Rate"
set key off
plot "results.txt" using 2:xtic(1) with boxes lt rgb "gray" """.format(numGames * 2)

try:
	while 1: # Will call BreakoutException to exit
		cumResults = {x:0 for x in playerNames}
		games = [runGame(playerNames[0], playerNames[1], counter) for x in range(numGames)]
		games += [runGame(playerNames[1], playerNames[0], counter) for x in range(numGames)]
		for out in games:
			if not any(out.values()):
				raise BreakoutException
			cumResults[playerNames[0]] += out[playerNames[0]]
			cumResults[playerNames[1]] += out[playerNames[1]]
		print("{} played {} games at n = {} to get {:.3f}%".format(playerNames[0], numGames*2, counter, cumResults[playerNames[0]] / sum(cumResults.values())))
		results.append((counter, cumResults[playerNames[0]] / sum(cumResults.values())))
		counter = counter + 1
except BreakoutException: # This is my goto equivalent :)
	with open("results.txt", "w") as f: # Write out the results to a buffer file
		f.write("\n".join("{},{}".format(*res) for res in results))
	os.system("echo '{}' | /usr/bin/gnuplot".format(gnu.replace("\n", "\\n")))
	os.system("rm results.txt") # Remove results buffer file
	print("Created graph.")