#
#Erick Tian
import sys
input = int(sys.argv[1])-31 if len(sys.argv)>1 and sys.argv[1].isdigit() else -1
output = ['/^0$|^100$|^101$/',                          ### 31
          '/^[01]*$/',                                  ### 32
          '/^[01]*0$/',                                 ### 33
          '/\w*[aeiou]\w*[aeiou]\w*/i',                 ### 34
          '/^1[01]*0$|^0$/',                            ### 35
          '/^[01]*110[01]*$/',                          ### 36
          '/^.{2,4}$/s',                                ### 37
          '/^[0-9]{3} *-? *[0-9]{2} *-? *[0-9]{4}$/',   ### 38
          '/^.*?d\w*\\b/im',                            ### 39
          '/^0$|^1$|^0[01]*0$|^1[01]*1$/',              ### 40

          r"/\b[pck]\w*/i",                                 ### 41
          r"/^.(..)*$/s",                                   ### 42 x_   dotall
          r"/^0([01][01])*$|^1[01]([01][01])*$/",           ### 43
          r"/^(0*(10)*)*1*$/",                              ### 44
          r"/^[\.xo]{64}$/i",                               ### 45
          r"/^[xo]*\.[xo]*$/i",                             ### 46
          r"/^(x+o*)*\.|\.(o*x+)*$/i",                      ### 47 x_ account for when u put just a corner    what does this mean - could corners count as connected?
          r"/^([bc]+a?[bc]*|[bc]*a[bc]*|[bc]*a?[bc]+)$/",   ### 48 x_   really long
          r"/^[bc]+$|^([bc]*[a][bc]*[a][bc]*)+$/",          ### 49 x_   base case no a's
          r"/^(2|20*)+(1[02]*1[02]*)*[02]*$|^(2|20*)*(1[02]*1[02]*)+[02]*$|^(2|20*)*(1[02]*1[02]*)*[02]+$/",                    ### 50 x_    solved w a buncha base cases

          r"/(.)\1{9}/s",                                                    ### 51 x_ needed dotall
          r"/(\w)\w*\1/i",                                                   ### 52 x_ ignorecase
          r"/\w*(\w)\1\w*/",                                                ### 53
          r"/\w*(\w)\w*\1\w*/i",                                             ### 54 x_ ignorecase
          r"/^[10]$|^([01])[01]*\1$/",                                      ### 55

          r"/\b(\w{3}cat|\w\wcat\w|\wcat\w\w|cat\w{3})\b/i",   ### 56 x_ ignorecase (also i dont think i did this the way it's supposed to be done)
          r"/^[01]$|(?<=^([01]))[01]*\1$/",                                      ### 57 x
          r"/^(?=([01]))[01]*\1$/",                                     ### 58
          r"/(?=\b(\w))\w*(?!\1\b)(?=[aeiou]\b)\w/i",                            ### 59 x
          r"/^((?!011)[01])*$/"]                                        ### 60 x

if input >= 0 and input<len(output): print(output[input])
else: print('invalid input')