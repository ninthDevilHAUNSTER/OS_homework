import random


class OSOperationError(Exception):
    def __init__(self, err='错误'):
        Exception.__init__(self, err)


class MFD(object):
    def __init__(self, username=None, file_index_pointer=None):
        self.username = username
        # print(file_index_pointer.__class__)
        if str(file_index_pointer.__class__) == "<class '__main__.UFDChain'>":
            self.file_index_pointer = file_index_pointer
        else:
            raise OSOperationError("file_index_pointer type must be UFDChain ")


class MFDChain(object):
    def __init__(self):
        self.MFD_chain = []
        self.user_index = []

    def append(self, MFD_block):
        self.MFD_chain.append(MFD_block)
        if MFD_block.username not in self.user_index:
            self.user_index.append(MFD_block.username)


class UFD(object):
    def __init__(self, filename=None, protect_code='000', file_length=None):
        self.filename = self.__checkfilename(filename)
        self.protect_code = self.__checkprotect_code(protect_code)
        self.file_length = file_length

        self.__readable, self.__writeable, self.__executable = self.__decoding_protect_code()

    def __checkprotect_code(self, code):
        if (code.__len__() == 3 and
                code[0] == '0' or code[0] == '1' and
                code[1] == '0' or code[1] == '1' and
                code[2] == '0' or code[2] == '1'):
            return code
        else:
            raise OSOperationError("文件权限码出错")

    def __decoding_protect_code(self):
        if len(self.protect_code) == 3:
            return self.protect_code[0] == '1', self.protect_code[1] == '1', self.protect_code[2] == '1'
        else:
            raise OSOperationError('protect code 出错')

    def __checkfilename(self, name):
        if name is None or len(name) > 20:
            raise OSOperationError('File Name Too Len')
        return name

    def check__readable(self):
        return self.__readable

    def check__writeable(self):
        return self.__writeable

    def check__executable(self):
        return self.__executable


class UFDChain(object):
    def __init__(self, owner=None, input_list=None):
        self.user = owner
        self.items = [None] * 10
        for i in input_list:
            if self.__check_if_class_valid(i):
                self.append(i)
        self.header = 0

    def append(self, ufd):
        try:
            input_index = self.items.index(None)
        except ValueError as e:
            return 0
        except Exception as e:
            raise OSOperationError(e.__str__())
        if self.__check_if_class_valid(ufd):
            self.items.pop(input_index)
            self.items.append(ufd)
            return 1
        else:
            return 0

    def delete(self, key):
        if self.items[key] is not None:
            self.items.pop(key)
            self.items.append(None)
            return 1
        else:
            raise OSOperationError("cannot del for item is None")

    def __check_if_class_valid(self, input_item):
        return True if str(input_item.__class__) == "<class '__main__.UFD'>" else False

    def __getitem__(self, item):
        self.header = item
        return self.items[self.header] if self.items[self.header] is not None else -100

    def __setitem__(self, key, value):
        if self.__check_if_class_valid(value):
            self.items[key] = value
        else:
            raise OSOperationError("The file must be UFD type")


class AFD(object):
    def __init__(self, open_file_code=None, open_file_protect_code=None,
                 read_or_write_pointe=None, open_file_name=None):
        self.open_file_code = open_file_code
        self.open_file_protect_code = open_file_protect_code
        self.read_or_write_pointer = read_or_write_pointe
        self.open_file_name = open_file_name

    def get_open_file_code(self):
        return self.open_file_code


class AFDChain(object):
    def __init__(self):
        self.item = [None] * 5

    def __getitem__(self, item):
        if item > 5:
            raise OSOperationError("超出最大读取文件个数")
        return self.item[item]

    def __setitem__(self, key, value):
        if key > 5:
            raise OSOperationError("超出最大读取文件个数")
        self.item[key] = value

    def find_index(self):
        if self.item.count(None) == 0:
            return -100
        for i in range(self.item.__len__()):
            if self.item[i] is None:
                return i
        raise OSOperationError("我不知道发生了啥，就是报错了")


class System(object):
    def __init__(self, user_MDF):
        self.__COMMAND_LIST = ["LIST", "CREATE", "DELETE", "OPEN", "CLOSE", "READ", "WRITE", "BYE", "STATE",
                               "LS", "TOUCH", "PS", "KILL", "OP", "VIM", "VI", "MV", "EXIT"]
        self.userUFD = user_MDF.file_index_pointer
        self.current_command = ""
        self.AFDChain = AFDChain()
        self.user_login_flag = True

    def list(self):
        print("YOUR FILE DIRECTORY")
        print("FILE NAME\tPROTECTION CODE\tLENGTH")
        for single_file in self.userUFD.items:
            if single_file is not None:
                print("{} \t {} \t {}".format(single_file.filename, single_file.protect_code, single_file.file_length))

    def create(self):
        filename = input("THE NEW FILE S NAME(LESS THAN 9 CHARS)?")  # F2
        protect_code = input("THE NEW FILE’S PROTECTION CODE?")  # 101
        file_length = input("THE NEW FILE' S LENGTH?")
        try:
            new_file_UFD = UFD(filename=filename, protect_code=protect_code, file_length=int(file_length))
        except Exception as e:
            print("THE NEW FILE CREATED FAILED")
            return 0
        if self.userUFD.append(new_file_UFD):
            print("THE NEW FILE IS CREATED.")
            YoN = input("ENTER THE OPEN MODE?")
            if "Y".lower() in YoN.lower():
                self.open(filename=filename)
        else:
            print("THE NEW FILE CREATED FAILED")
        # pass

    def delete(self, filename=""):
        index = 0
        for i in self.AFDChain.item:
            if i is not None and i.open_file_name == filename:
                print("FIND FILE OPEN CLOSE FILE FIRST")
                self.close(index)
            index += 1
        index = 0
        for i in self.userUFD.items:
            if i is not None and i.filename == filename:
                self.userUFD.delete(index)
                return 1
            index += 1
        print("FILE DELETE FAIL")
        return 0

    def open(self, filename=""):
        for i in self.userUFD.items:
            if i is not None and i.filename == filename:
                index = self.AFDChain.find_index()
                while 1:
                    file_mode = input("ENTER THE OPEN MODE? R<read> | W<write>")
                    # print(file_mode)
                    if "r" in file_mode.lower():
                        # pass
                        self.AFDChain[index] = AFD(open_file_code=index,
                                                                       open_file_protect_code=i.protect_code,
                                                                       read_or_write_pointe=0,
                                                                       open_file_name=i.filename)
                    elif "w" in file_mode.lower():
                        # pass
                        self.AFDChain[index] = AFD(open_file_code=index,
                                                                       open_file_protect_code=i.protect_code,
                                                                       read_or_write_pointe=1,
                                                                       open_file_name=i.filename)
                    else:
                        print("INPUT ERROR PLEASE INPUT R or W")
                        continue
                    print("THIS FILE IS OPENED,ITS OPEN NUMBER IS {}".format(index))
                    return 1
        print("UNVALID FILENAME!")
        return 0

    def ps(self):
        print("------------- OPEN FILE INDEX -------------")
        print("open file id\t\topen file name\t\topen file protect code\t\tread or write pointer")
        index = 0
        for i in self.AFDChain.item:
            if i is None:
                print("{}\t\t\t\t{}\t\t\t\t{}\t\t\t\t{}".format(index, "*******", "***", "?"))
                index += 1
            else:
                print("{}\t\t\t\t{}\t\t\t\t{}\t\t\t\t{}".
                      format(index, i.open_file_name, i.open_file_protect_code, i.read_or_write_pointer))
                index += 1
        print("------------- #### #### #### --------------")

    def bye(self):
        self.user_login_flag = False
        print("GOOD BYE")

    def close(self, open_file_code=0):
        if self.AFDChain[open_file_code] is None:
            print("ERROR MESSAGE: NO THIS OPEN FILE !!!")
            return 0
        else:
            self.AFDChain[open_file_code] = None

    def read(self, open_file_code=0):
        if self.AFDChain[open_file_code] is None:
            print("ERROR MESSAGE: NO THIS OPEN FILE !!!")
            return 0
        elif self.AFDChain[open_file_code].open_file_protect_code[0] == '0':
            print("ERROR MESSAGE:IT IS NOT ALLOWED TO READ THIS FILE !!!")
            return 0
        elif self.AFDChain[open_file_code].read_or_write_pointer == 0:
            print("FILE CONTENT :")
            print("........................")
            # 小生的系统比较笨，只能要么读，要么写，不能两个通道一起开
            return 1
        else:
            print("ERROR MESSAGE:THE FILE IS NOT OPEN FOR READ !!!")

    def write(self, open_file_code=0):
        if self.AFDChain[open_file_code] is None:
            print("ERROR MESSAGE: NO THIS OPEN FILE !!!")
            return 0
        elif self.AFDChain[open_file_code].open_file_protect_code[1] == '0':
            print("ERROR MESSAGE:IT IS NOT ALLOWED TO READ THIS FILE !!!")
            return 0
        elif self.AFDChain[open_file_code].read_or_write_pointer == 1:
            # 小生的系统比较笨，只能要么读，要么写，不能两个通道一起开
            write_file_len = input("HOW MANY CHARACTERS TO BE WRITTEN INTO THAT FILE?")
            tmp_name = self.AFDChain[open_file_code].open_file_name
            for i in self.userUFD.items:
                if i is not None and i.filename == tmp_name:
                    i.file_length += int(write_file_len)
            return 1
        else:
            print("ERROR MESSAGE:THE FILE IS NOT OPEN FOR READ !!!")

    def main_recurtion(self):
        self.current_command = input("COMMAND NAME?")
        self.__read_command(self.current_command)

    def __read_command(self, c):
        if c.upper() not in self.__COMMAND_LIST:
            print("COMMAND NAME GIVEN IS WRONG!\n"
                  "IT SHOULD BE ONE OF FOLLOWING : CREATE(touch), DELETE(mv), OPEN(op), CLOSE(kill), READ(cat),"
                  " WRITE(vim), LIST(ls),STATE(ps), BYE(exit).TRY AGAIN")
        elif c.lower() == "list" or c.lower() == "ls":
            self.list()
        elif c.lower() == "state" or c.lower() == "ps":
            self.ps()
        elif c.lower() == "bye" or c.lower() == "exit":
            self.bye()
        elif c.lower() == "create" or c.lower() == "touch":
            self.create()
        elif c.lower() == "delete" or c.lower() == "mv":
            open_file_name = input("PLEASE INPUT OPEN FILE NAME")
            self.delete(open_file_name)
        elif c.lower() == "open" or c.lower() == "op":
            open_file_name = input("PLEASE INPUT OPEN FILE NAME")
            self.open(open_file_name)
        elif c.lower() == "read" or c.lower() == "cat":
            try:
                open_file_code = int(input("OPEN FILE NUMBER?"))
                self.read(open_file_code=open_file_code)
            except Exception as e:
                raise OSOperationError(e.__str__())
        elif c.lower() == "write" or c.lower() == "vi" or c.lower() == "vim":
            try:
                open_file_code = int(input("OPEN FILE NUMBER?"))
                self.write(open_file_code=open_file_code)
            except Exception as e:
                raise OSOperationError(e.__str__())
        elif c.lower() == "close" or c.lower() == "kill":
            try:
                open_file_code = int(input("THE OPENED FILE NUMBER TO BE CLOSED?"))
                self.close(open_file_code=open_file_code)
            except Exception as e:
                raise OSOperationError(e.__str__())


www_UFD = UFDChain(owner='www', input_list=[
    UFD(filename='Flag', protect_code="000", file_length=20),
    UFD(filename='ShaobaoNiubi', protect_code="111", file_length=random.randint(20, 50)),
    UFD(filename='index.php', protect_code="101", file_length=random.randint(20, 50)),
    UFD(filename='config.php', protect_code="101", file_length=random.randint(20, 50)),
    UFD(filename='database.py', protect_code="101", file_length=random.randint(20, 50)),
])
websource_UFD = UFDChain(owner='wwwroot', input_list=[
    UFD(filename='config.js', protect_code="000", file_length=random.randint(200, 500)),
    UFD(filename='jquery.js', protect_code="111", file_length=random.randint(200, 500)),
    UFD(filename='md5.js', protect_code="111", file_length=random.randint(200, 500)),
    UFD(filename='index.js', protect_code="111", file_length=random.randint(200, 500)),
    UFD(filename='main.js', protect_code="111", file_length=random.randint(200, 500)),
])

root_UFD = UFDChain(owner='root', input_list=[
    UFD(filename='shadow', protect_code="000", file_length=random.randint(200, 500)),
    UFD(filename='passwd', protect_code="111", file_length=random.randint(200, 500)),
    UFD(filename='hosts', protect_code="111", file_length=random.randint(200, 500)),
    UFD(filename='docker', protect_code="111", file_length=random.randint(200, 500)),
    UFD(filename='resource', protect_code="111", file_length=random.randint(200, 500)),
])

fuli_UFD = UFDChain(owner='shaobao', input_list=[
    UFD(filename='No thins.txt', protect_code="110", file_length=20),
    UFD(filename='{}.png'.format(random.randint(11111, 99999)), protect_code="110",
        file_length=random.randint(20, 50)),
    UFD(filename='{}.png'.format(random.randint(11111, 99999)), protect_code="110",
        file_length=random.randint(20, 50)),
    UFD(filename='{}.png'.format(random.randint(11111, 99999)), protect_code="110",
        file_length=random.randint(20, 50)),
    UFD(filename='{}.png'.format(random.randint(11111, 99999)), protect_code="110",
        file_length=random.randint(20, 50)),
    UFD(filename='{}.png'.format(random.randint(11111, 99999)), protect_code="110",
        file_length=random.randint(20, 50)),
    UFD(filename='{}.png'.format(random.randint(11111, 99999)), protect_code="110",
        file_length=random.randint(20, 50)),
    UFD(filename='{}.png'.format(random.randint(11111, 99999)), protect_code="110",
        file_length=random.randint(20, 50)),
    UFD(filename='{}.png'.format(random.randint(11111, 99999)), protect_code="110",
        file_length=random.randint(20, 50)),
])

guest_UFD = UFDChain(owner='guest', input_list=[])

mdf_chain = MFDChain()

mdf_chain.append(MFD(username="www", file_index_pointer=www_UFD))
mdf_chain.append(MFD(username="wwwroot", file_index_pointer=websource_UFD))
mdf_chain.append(MFD(username="shaobao", file_index_pointer=fuli_UFD))
mdf_chain.append(MFD(username="root", file_index_pointer=root_UFD))
mdf_chain.append(MFD(username="guest", file_index_pointer=guest_UFD))

# print(str(UFD(filename='1',protect_code='111',file_length=123).__class__)=="<class '__main__.UFD'>")

while 1:
    input_username = input("PLEASE INPUT USER NAME")
    user_login_flag = False
    if input_username in mdf_chain.user_index:
        print("WELCOME {}".format(input_username.upper()))
        user_login_flag = True
        system = System(user_MDF=mdf_chain.MFD_chain[mdf_chain.user_index.index(input_username)])
    else:
        continue
    while user_login_flag:
        system.main_recurtion()
        user_login_flag = system.user_login_flag
