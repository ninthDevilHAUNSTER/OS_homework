import os
import sys
from getopt import getopt

sys.path.append('../')

from config.config import *


def cat(args):
    file = args[0]
    if os.path.exists(os.path.abspath(os.curdir) + '\\' + file):
        print(open(
            os.path.abspath(os.curdir) + '\\' + file, 'rb')
              .read().decode('utf8'))
        # 避免GBK编码的问题
    else:
        print(BSHELL_ERROR['2'].format(file))
    return SHELL_STATUS_RUN
