#
#Erick Tian
import sys
input = int(sys.argv[1])-31 if sys.argv[1].isdigit() else -1
output = ['/^0$|^100$|^101$/',                          ### 31
          '/^[01]*$/',                                  ### 32
          '/^[01]*0$/',                                 ### 33
          '/\w*[aeiou]\w*[aeiou]\w*/i',                 ### 34
          '/^1[01]*0$|^0$/',                            ### 35
          '/^[01]*110[01]*$/',                          ### 36
          '/^.{2,4}$/s',                                ### 37
          '/^[0-9]{3} *-? *[0-9]{2} *-? *[0-9]{4}$/',   ### 38
          '/^.*?d\w*\\b/im',                            ### 39
          '/^0$|^1$|^0[01]*0$|^1[01]*1$/']              ### 40
if input >= 0 and input<len(output): print(output[input])
else: print('invalid input')