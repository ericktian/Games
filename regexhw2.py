#
#Erick Tian
import sys
input = int(sys.argv[1])-41 if sys.argv[1].isdigit() else -1
output = [r"/\b[pck]\w*/i",                                 ### 41
          r"/^.(..)*$/",                                    ### 42
          r"/^0([01][01])*$|^1[01]([01][01])*$/",           ### 43
          r"/^((?!110)[01])*$/",                            ### 44
          r"/^[\.xo]{64}$/i",                               ### 45
          r"/^[xo]*\.[xo]*$/i",                             ### 46
          r"/^x+o*\.|\.o*x+$/i",                            ### 47
          r"/^[bc]*[a][bc]*$/",                             ### 48
          r"/^([bc]*[a][bc]*[a][bc]*)+$/",                  ### 49
          r"/^[02]*([02]*1[02]*1[02]*)*[02]*$/"]            ### 50
if input >= 0 and input<len(output): print(output[input])
else: print('invalid input')