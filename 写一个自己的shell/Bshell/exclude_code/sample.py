# def command_string2array(string):
#     tmp = string.split(' ')
#     if tmp.__len__() == 1:
#         return [tmp]
#     simple_array = [tmp[0]]  # sys.arg[0]
#     params = []
#     for i in tmp:
#         if '-' in i:
#             params.append(tmp.index(i))
#     if params.__len__() != 0:
#         # 如果有 - 这种东东
#         if params[0] > 1:
#             for z in range(1, params[0]+1):
#                 simple_array.append(tmp[z])
#         for id in range(0,params.__len__()):
#             simple_array.append([])
#
#     else:
#         return simple_array  # sys.arg[0] :: ls sys.arg[1] ./
#
#
# if __name__ == '__main__':
#     command_string2array("ls baidu -l a -s shaobao -g a a")

import sys, getopt

try:
    opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
except getopt.GetoptError:
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        sys.exit()
    elif opt in ("-i", "--ifile"):
        inputfile = arg
    elif opt in ("-o", "--ofile"):
        outputfile = arg
