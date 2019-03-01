import sys
import os

# 日志
HISTORY_PATH = os.path.expanduser('~') + os.sep + '.bsh_history'


# 系统变量
SYSTEM_VARIABLES = {
    '$PWD': '',
}
# 状态
SHELL_STATUS_STOP = 0
SHELL_STATUS_RUN = 1

# 错误提示
BSHELL_ERROR= {
    '1':"[BShell Error 1] 系统找不到指定的命令 : \'{}\'",
    '2': "[BShell Error 2] 系统找不到指定的文件 : \'{}\'",
}

