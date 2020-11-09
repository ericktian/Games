#
#Erick Tian
import sys
input = int(sys.argv[1])-56 if sys.argv[1].isdigit() else -1
output = [r"/\b\w{3}cat\b|\b\w\wcat\w\b|\b\wcat\w\w\b|\bcat\w{3}\b/",   ### 56
          r"/[01]*([01])(?<=\1)/",                                      ### 57
          r"/^(?=([01]))[01]*\1$/",                                     ### 58
          r"/(?=^(\w))(?=\1$)(?=[aeiou]$)/",                            ### 59
          r"/^((?!011)[01])*$/"]                                        ### 60
if input >= 0 and input<len(output): print(output[input])
else: print('invalid input')