#
#Erick Tian
import sys
input = int(sys.argv[1])-51 if sys.argv[1].isdigit() else -1
output = [r"/(.)\1{9}/",                                                    ### 51
          r"/(\w)\w*\1/",                                                   ### 52
          r"/\w*(\w)\1\w*/",                                                ### 53
          r"/\w*(\w)\w*\1\w*/",                                             ### 54
          r"/^[10]$|^([01])[01]*\1$/",                                      ### 55
          r"/\b\w{3}cat\b|\b\w\wcat\w\b|\b\wcat\w\w\b|\bcat\w{3}\b/"]       ### 56
if input >= 0 and input<len(output): print(output[input])
else: print('invalid input')