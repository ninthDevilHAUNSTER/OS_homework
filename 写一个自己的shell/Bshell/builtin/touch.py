import os
import sys
from getopt import getopt

sys.path.append('../')

from config.config import *


def touch(args):
    file = args[0]
    abs_path = os.path.abspath(os.curdir) + '\\' + file
    if os.path.exists(abs_path):
        sys.stdout.write("{} is excist override ? (Yes/No)".format(file))
        sys.stdout.flush()
        a = sys.stdin.readline()  # get_comln
        if "y" in __import__('shlex').split(a)[0].lower().lower():
            open(abs_path, 'w').close()
        # print(open(
        #     os.path.abspath(os.curdir) + '\\' + file, 'rb')
        #       .read().decode('utf8'))
        # 避免GBK编码的问题
    else:
        open(abs_path, 'w').close()
        # print(BSHELL_ERROR['2'].format(file))
    return SHELL_STATUS_RUN
