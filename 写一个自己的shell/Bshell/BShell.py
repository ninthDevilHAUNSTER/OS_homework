from __future__ import absolute_import
import os
import sys
import shlex
import getpass
import socket
import signal
import subprocess
import platform

from config.config import *
from builtin import *


class BShell(object):
    def __init__(self):
        '''
        启动shell的初始化
        :return:
        '''
        self.variables = SYSTEM_VARIABLES
        self.pwd = os.getcwd()
        os.chdir(self.pwd)
        self.variables['$PWD'] = self.pwd
        # Hash map to store built-in function name and reference as key and value
        self.built_in_cmds = {}
        self.init_command()

    def init_command(self):
        '''
        装载指令
        :return:
        '''
        self.__register_command('cd', cd)
        self.__register_command('logout', logout)
        self.__register_command('exit', logout)
        self.__register_command('cat', cat)
        self.__register_command('history', history)
        self.__register_command('mkdir', mkdir)
        self.__register_command('ls', ls)
        self.__register_command('ll', ls)
        self.__register_command('touch', touch)

    def __register_command(self, name, func):
        self.built_in_cmds[name] = func

    def get_simcom(self, string):
        '''
        将输入命令化为简单命令；生成简单数组
        :return:`
        '''
        return shlex.split(string)

    def execute(self, cmd):
        '''
        执行当前简单命令
        :param command_array:
        :return:
        '''
        with open(HISTORY_PATH, 'a') as history_file:
            history_file.write(' '.join(cmd) + os.linesep)

        if cmd:
            cmd_name = cmd[0]
            cmd_args = cmd[1:]

            if cmd_name in self.built_in_cmds:
                return self.built_in_cmds[cmd_name](cmd_args)
            else:
                print(
                    BSHELL_ERROR['1'].format(cmd_name)
                )
                return SHELL_STATUS_RUN
        return SHELL_STATUS_RUN

    def display_cmd_prompt(self):
        '''
            # Display a command prompt as `[<user>@<hostname> <dir>]$ `
        :return:
        '''
        # Get user and hostname
        user = getpass.getuser()
        hostname = socket.gethostname()

        # Get base directory (last part of the curent working directory path)
        cwd = os.getcwd()
        base_dir = os.path.basename(cwd)

        # Use ~ instead if a user is at his/her home directory
        home_dir = os.path.expanduser('~')
        if cwd == home_dir:
            base_dir = '~'

        # Print out to console
        sys.stdout.write("[%s@%s %s]$ " % (user, hostname, base_dir))
        sys.stdout.flush()

    def ignore_signals(self):
        '''
        # Ignore Ctrl-Z stop signal
        # Ignore Ctrl-C interrupt signal
        :return:
        '''
        if platform.system() != "Windows":
            signal.signal(signal.SIGTSTP, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def shell_loop(self):
        status = SHELL_STATUS_RUN

        while status == SHELL_STATUS_RUN:
            self.display_cmd_prompt()
            # Ignore Ctrl-Z and Ctrl-C signals
            self.ignore_signals()

            try:
                cmd = sys.stdin.readline()  # get_comln
                cmd_tokens = self.get_simcom(cmd)
                status = self.execute(cmd_tokens)
            except:
                _, err, _ = sys.exc_info()
                print(err)
