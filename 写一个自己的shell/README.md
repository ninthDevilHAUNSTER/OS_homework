# 操作系统的实现

python start.py即可

东西都是内置的

参考了yosh的部分代码

支持的操作如下

```python
        self.__register_command('cd', cd)
        self.__register_command('logout', logout)
        self.__register_command('exit', logout)
        self.__register_command('cat', cat)
        self.__register_command('history', history)
        self.__register_command('mkdir', mkdir)
        self.__register_command('ls', ls)
        self.__register_command('ll', ls)
        self.__register_command('touch', touch)
```