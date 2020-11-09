#!/usr/bin/python3
#
# Othello Lab A grader
#
# Original development Torbert, 18 Dec 2015: mod.py
# updated by Gabor, Jan - Feb, 2016 to deal with timeouts: modmod.py
# further updates by Gabor, Jan, 2018 to facilitate grading
# and Kulkarni, 19 Jan 2018 to streamline calling
#
# usage:
# python3 validator.py latestScript
#
# will run all scripts which were modified at or after the modification
# that the final script matching latestScript has.
# also writes to file summary.txt
##################################################

# from subprocess import Popen
from subprocess import run, PIPE, TimeoutExpired, check_output
from time       import time, ctime, strptime, mktime, perf_counter
from os         import path, remove
import sys, re, os, random
import subprocess
# import subprocess    # linux evidently needs this with TimeoutExpired

##################################################
timeLeft = 2    # number of seconds allowed per move
help     = "Usage: python3 grader.py [oldestScriptPrefix]"

startTime = time()
pyver = re.sub(' [^Z]*', "", sys.version)
print ("{} running under python version {}".format(path.basename(__file__), pyver))


def restrictedP(fn, restrictedSet):
  # returns the set of elements from restricted set that prefix fn
  return {rs for rs in restrictedSet if rs.lower()==fn[:len(rs)].lower()}


def indent(text, amt):
  return " "*amt + ("\n" + " "*amt).join(text.splitlines())


rexPastSmry = re.compile("^(\\S+)\\s*from (.+20\\d\\d) play(?:ing|ed) (\\d+) games => (.+) for (.+)$")
rexPct      = re.compile("^(\\d+[.]?\\d*)\\s*%")

def summarySlurp():
  fn = "summary.txt"
  if not path.isfile(fn): return {}
  aLines = open(fn, "r").read().splitlines()
  aRes = {}
  for line in aLines:
    if not line or line[0]==" ": continue
    if line[:9] == "Skunk for": continue
    if line[:9] == "Test run ": continue
    grps = rexPastSmry.search(line)
    if not grps: continue
    flName = grps.group(1)
    flDate = grps.group(2)
    gameCt = int(grps.group(3))
    person = grps.group(5)
    result = grps.group(4)
    grpsPct= rexPct.search(result)
    pct = float(grpsPct.group(1)) if grpsPct else -1
#    print ("result: {}, pct: {}".format(result, pct))

    if flName not in aRes: aRes[flName] = []
#    aRes[flName] = [pct, mktime(strptime(flDate)), gameCt]
    aRes[flName] = [pct, flDate, gameCt]

#  exit("\n".join(sorted(["{}: {}".format(fl, aRes[fl]) for fl in aRes])))


  return aRes
    

def getStudents():
  fName = "nevek.txt" #fName = "../nevek/nevek.txt"
  aNames = open(fName, "r").read().splitlines()
  return aNames


def personFromScript(scriptFile, aStudents):
  # this section will need fixing if we have identical last names
  lscript = scriptFile.lower()
  lscript3 = lscript[:-3]            # remove .py extension
  aXact = [nev for nev in aStudents if lscript3+" "==nev[:len(lscript3)+1].lower()]   # try for an exact last name match (for short last names)
  if len(aXact)==1: person = aXact[0]
  elif len(aXact)>1:person = "Multiple exact names"
  else:
    aMatch = [nev for nev in aStudents if lscript3==nev[:len(lscript3)].lower()]
    if len(aMatch)==1: person = aMatch[0]
    elif not aMatch: person = "No matching person"
    else: person = "Duplicate matching names"
  if person[0] == "p": person = "p{}: {} {}".format(person[1], person[person.find(" ")+1:], person[2:person.find(" ")])
  return person


def findFile(*fileSpec):
  filesInDir, matchingFiles = set(), set()
  mypath = os.getcwd()
  for (dirpath, dirnames, filenames) in os.walk(mypath):
    filesInDir = {*filenames}  # Gets all files in the path
    break
  if not fileSpec: return filesInDir

  for fs in fileSpec:
    if fs.find('.') >= 0:             # If extension provided, then we must mean that file sans capitalization
      if path.isfile(fs): matchingFiles.add(fs)
    else:                            # If unique prefix is provided
      fs = fs.lower()
      matchingFiles |= {s for s in filesInDir if s[:len(fs)].lower()==fs}
  return matchingFiles


def rngLim(c, d, n):
  if (abs(d) - 1) % (n-1):    # if diagonal direction
    return n-max(n-1-c%n if (d-1)%n else c%n, n-1-c//n if d<0 else c//n)
  return (n if d>0 else 1) - (d // abs(d)) * (c%n if d%n else c//n)




def legalMoves(othelloBoard, token):
  dot = '.'
  moves = {}
  for idx in [idx for idx,tkn in enumerate(othelloBoard) if tkn==dot]:
    for dir, lim in legalMoves.dirrng[idx]:
      for p in range(idx+dir,lim,dir):
        if othelloBoard[p]==".": break
        if othelloBoard[p]==token:
          if p==idx+dir: break
          if idx not in moves: moves[idx] = set()
          moves[idx].update(range(idx+dir,p,dir))
          break
  return moves


def findLineWithPhrase(strRex, strSubject):
  grps = re.search(strRex, strSubject)
  if not grps: return -1
  return strSubject[:len(grps.group(0))].count("Z")


listOfTests = [
  ["OOOOOXXXOXOOOOXOOOOXOXX.OOXXXXXOOOXXXXXO.OXXXOXOOOXXOXOOOXXOOOOO x", 2,  {23}],
  ["XXX.OXXX.XXXXXXXXXXXXOXXXXXXOXOXXXXOXOXXXXOXOXXX.XXOXXXXOXXXXXXX o", -6, {3}],
  ["...ooooo ox.xoooo oxxxxooo oxoxxxoo oxxxxooo oxxoxooo oxxxxxoo oooooooo O", 42, {1}],
  ["oooooo.. xoxxoo.. xxooooxx xxxoooxx xxoxooxx xxxoxoox .xxxxxxx xxxxxxxx o", 0, {48}],
  ["O.X.O.XOXO..O.OXXOOOOOXXXOXOOXXXXOOXXXXXXOOXXXXXXXXXXXXXXXXXXXXX x", 50, {5}],
  ["XXXXXXXOXXXXXXXOXXXXXXXOXXOXXX.OXOXOOO..XOOXO...XXXXXXX.XXXXXXXX X", 47, {30}],
  ["....OOOOO...XXOOOOXXX.OOOXOXXOOOOOOOXOOOOOOOXXOOOOOOOOXOOOOOOOOO O", 60, {21, 9}],           # 21, 11, 9 ...
]

listOfTests = [
  ["OOOOOOOOO.XXXXO.OOXXXXX.OOXXXXO.OOXXXXXXOOOOOX..XXXXOOO.XXXXXXX. x", 0,  {9}],                     # 8 free
  ["OX.O.XX.OXXXXXXOOOXOOOOXOOXXOOX.OOOXOXXOO.OOOXXX.OOOOOXXXOO.OX.. o", 14, {7}],                     # 9 free
  ["X.OXXX..X.OOXXX.XOOXOXOOXXOOXOOOXXOXOXOOXOXOOXOOOOOOOO....OOOOO. X", 4,  {9}],                     # 10 free
  ["...OOOOO..XXXXXO.XOOOOXOXOOOOOXOXOOOXOXOXOOXOXOO..OOOOXO..OOOO.X O", 7,  {62}],                    # 11 free
  ["..XXXXXX.OOXXOOXXXOXOOOX..OOOXOX..OOOXOX.OOOXOOXOOOXXOOX..OXXO.. x", 26, {8, 25, 40, 57, 62}],     # 12 free
  ["XXXXOOOOOXXXOXO.OXXOOXOXOXXXOX.XOOXXX..XOOOXXX..OOOOOX..OOO..... o", -6, {46, 30}],                # 13 free
  ["XXXXXXXXXXXXOXXXXXXOXOXXXXOXOOOXXXOOOO.XXXOO.O.XXXO..O..X....... x", 61, {58}],                    # 14 free
#  [".........O.X...O.OOXXOOOXXXOXXXOXXXOOXXOXXXXXOXOXXXXXOOOXXXXXXXO X", 16, {12, 13}],                # 14 free
]




def boardCheck2D(inAsLine, brd1D):
  brd2D = "Z".join([brd1D[leftEdge:leftEdge+8] for leftEdge in range(0,len(brd1D),8)]).upper()
  act3 = inAsLine.replace("*",".").replace("+",".")
  act4 = re.sub("[^xXoO.Z]", "", act3)
  act5 = re.sub("Z+", "Z", act4)
  bp2d = act5.upper().rfind(brd2D)
  return bp2d >= 0 


def possibleMovesErr(inAsLine, lm):
  inAsLine = re.sub("\\s+", " ", inAsLine.replace(",", " "))
  if not re.search("^.*(possible|legal) moves?\\b", inAsLine, re.I): return "Legal/possible moves phrase not found"
  grps = re.search("^.*(possible|legal)\\s+moves?.+?((([1-9]\\d*|0) )*([1-9]\\d*|0(?=\\D|$)))", inAsLine, re.I)
  if not grps: return "Legal/possible moves format was incorrect"
  pm = {int(i) for i in grps.group(2).split(" ")}
  lm = {*lm}
  if lm != pm: return "Legal/possible moves of {} was incorrect".format(grps.group(2))
  if len(lm) != len(pm) or len(lm & pm) != len(lm): return "Legal/possible moves of {} was incorrect".format(pm)
  return ""    # success


def heuristicErr(inAsLine, lm):
  if not re.search("^.*heuristic", inAsLine, re.I): return "Heuristic word not found"
  grps = re.search("^.*heuristic.+?([1-9]\\d*|0(?=\\D|$))", inAsLine, re.I)
  if not grps: return "Heuristic move was missing"
  if int(grps.group(1)) not in lm: return "Heuristic move of {} was incorrect".format(grps.group(1))
  return ""


def negamaxErr(inAsLine, score, mvSet):
  if not re.search("^.*(nega|mini)max", inAsLine, re.I): return "Negamax/Minimax word not found"
  grps = re.search("^.*(nega|mini)max.*?(-?[1-9]\\d*|0(?=\\D|$)).*\\D(-?[1-9]\\d*|0(?=\\D|$))", inAsLine, re.I)
  if not grps: return "Negamax/Minimax score or move not found"
  if int(grps.group(2)) != score: return "Negamax/Minimax score of {} does not match".format(grps.group(2))
  if int(grps.group(3)) not in mvSet: return "Negamax/Minimax move of {} was incorrect".format(grps.group(3))
  return ""



def performValidation(script, test):
  # test[0] has board and token as single command line arg
  # test[1] has best score to be achieved
  # test[2] has set of moves that can get one to that score
  test[0] = test[0][:-2].replace(" ", "") + " " + test[0][-1]
  myargs = [ '"{}"'.format(sys.executable) , "-u", '"{}"'.format(script), test[0]]
  tmOut = 60
  timedOut = False

#  print("About to run {}".format(" ".join(myargs)))

  if os.name == "posix":
    try:
      xcmd = "timeout {} {}".format(tmOut, " ".join(myargs))
      x = check_output(xcmd, shell=True)
    except Exception as exc:        # should be a subprocess.CalledProcessError exception
      timedOut = True
      errOut    = "{}".format(exc)
      actualOut = exc.stdout.decode()     # exc.stderr is not known
    else:
      errOut = ""
      actualOut = x.decode()
  else:
    try:
      po = run ( " ".join(myargs), shell=True , timeout=tmOut, stdout=PIPE, stderr=PIPE)
    except TimeoutExpired as timeErr:
      timedOut = True
      errOut    = timeErr.stderr.decode()
      actualOut = timeErr.stdout.decode()
#     print (dir(timeErr))
    else:
      errOut =    po.stderr.decode()
      actualOut = po.stdout.decode()
  
  # returns [test, "Error: timeout\n" + indent(errOut), "Output:\n" + indent(actualOut)]

  if timedOut: return [test, "Error: timeout\n" + indent(errOut,2), "Output:\n" + indent(actualOut,2)]
  if errOut:   return [test, "Other Error:\n" + indent(errOut,2), "Output:\n" + indent(actualOut,2)]


  # check whether 2D board is given
  act1 = actualOut.replace("Z", "") + "Z"
  act2 = "Z".join(act1.splitlines())        # makes it a string on one line
  act3 = re.sub("\\d*[.]\\d+", " ", act2)   # removes decimal numbers - does not remove 31. as it might be sentence end
  token = test[0][-1]
  brd1D = test[0][:-2].replace(" ","")
  if not boardCheck2D(act3, brd1D):
    return [test, "Correct 2D board not found:\n" + indent(actualOut,2), ""]

  # legal moves section
  lm = legalMoves(brd1D.upper(), token.upper())
  pme =  possibleMovesErr(act3, lm)
  if pme: return [test, pme + "\n" + indent(actualOut,2), ""]

  # heuristic moves section
  hme = heuristicErr(act3, lm)
  if hme: return [test, hme + "\n" + indent(actualOut,2), ""]

  # negamax section
  nme = negamaxErr(act3, test[1], test[2])
  if nme: return [test, nme + "\n" + indent(actualOut,2), ""]

  return [test, "", ""]        # success!



def validateScript(script):
  passCt = 0
  smry = ""
  for test in listOfTests:
    testStart = perf_counter()
    valRes = performValidation(script, test)
    if not valRes[1]:
      passed = "Passed: {}  in {}s".format(test[0], "{}".format(perf_counter()-testStart)[:6])
      smry += ("\n" if smry else "") + passed
      print("  " + passed, flush=True)
      passCt += 1
    else:
      token = test[0][-1]
      brd1D = test[0][:-2].replace(" ","")
      lm = legalMoves(brd1D.upper(), token.upper())
      failed = "Failed: {}  in {}s".format(test[0], "{}".format(perf_counter()-testStart)[:6])
      failed += "\n  Expected: legalMoves: {}; negamax score {} and move from {}".format({*lm.keys()}, test[1], test[2])
      failed += "\n" + indent(valRes[1], 2)
      if valRes[2]: failed += "\n  Actual out:" + indent(valRes[2],2)
      smry += ("\n" if smry else "") + failed
      print(indent(failed, 2), flush=True)
  return smry, passCt, len(listOfTests)
#  append results to summary file
#  maintain student score


aStuds = getStudents()

# get all matching files in this directory
listOfScripts = sorted([(path.getmtime(s), s) for s in findFile(sys.argv[1]) if s[-3:]==".py"])
if not listOfScripts: print("No scripts found\nUsage: validator.py [scriptSpec ...]"); exit(0)

pastTests = summarySlurp()

# Constants for calculating legalMoves
sL = 8
dirs = [{h+v for h in [-1,0,1] for v in [-sL,0,sL] for b in [c+h+v+h+v] \
               if (b>=0)*(b<sL*sL)*((b%sL-c%sL)*h>=0)}-{0} for c in range(sL*sL)]
# the direction together with the boundary of where one must check for bracketing
legalMoves.dirrng = [[(dir,idx+rngLim(idx,dir,sL)*dir) for dir in setOfDirs] for idx,setOfDirs in enumerate(dirs)]


for fltime, script in listOfScripts:
  student = personFromScript(script, aStuds)
  print("Running {} validation tests on script {} of {} for person {}".format(len(listOfTests), script, ctime(fltime), student))
  smry, passCt, outOf = validateScript(script)
#  print("Score {}/{} for {} => {}\n{}\n\n".format(passCt, outOf, script, student, smry))
  res = "Score {}/{} on {} of {} for person {}".format(passCt, outOf, script, ctime(fltime), student)
  print(res)










