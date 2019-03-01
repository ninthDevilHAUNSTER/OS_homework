import os
import sys

sys.path.append('../')

from config.config import *

import getopt
import time


def ls(args):
    A, args = getopt.getopt(args, 'a', ['all='])
    # print(args)
    if args.__len__() == 0:
        args = os.curdir
    else:
        args = args[0]

    if os.path.exists(os.path.abspath(args)):
        abs_path = os.path.abspath(args)
    else:
        return SHELL_STATUS_RUN

    show = False
    for name, value in A:
        if name in ("-a", "--all") and show == False:
            print("file name \t filesize \t last modify time")
            try:
                for current_file in os.listdir(abs_path):
                    if os.path.isfile(abs_path + "\\" + current_file):
                        mtime1 = os.path.getmtime(abs_path + "\\" + current_file)
                        size = os.path.getsize(abs_path + "\\" + current_file)
                        print('{} \t {:.2f}KB \t {} \t'.format(
                            current_file, size / 1024, time.asctime(time.localtime(mtime1))))
                    else:
                        print(current_file)
                show = True
            except (FileExistsError, FileNotFoundError) as e:
                print(e)
    if show == False:
        try:
            for current_file in os.listdir(abs_path):
                print(current_file)
        except (FileExistsError, FileNotFoundError) as e:
            print(e)
    return SHELL_STATUS_RUN
