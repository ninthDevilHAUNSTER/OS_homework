import numpy as np
import random
from matplotlib import pyplot


class MemoryBlock(object):
    def __init__(self):
        self.VIRTUAL_MEMORY_SIZE = 32 * 2 ** 10
        self.PAGE_SIZE = 1024
        self.GIVEN_ARRAY_LEN = 256
        self.size = 1
        self.assign = 4
        self.A = []
        self.PAGE = []
        self.eliminate_Alg = None

    def update_VIRTUAL_MEMORY_SIZE(self, value):
        self.VIRTUAL_MEMORY_SIZE = value

    def update_PAGE_SIZE(self, value):
        self.PAGE_SIZE = value

    def update_assign(self, value):
        self.assign = value

    def init_with_random_num(self):
        self.GIVEN_ARRAY_LEN = int(input(">> PLEASE INPUT GIVEN_ARRAY_LEN")) // 1
        # self.GIVEN_ARRAY_LEN = 40  # TODO :: DELETE  | JUST FOR TEST
        self.GIVEN_ARRAY_LEN = self.GIVEN_ARRAY_LEN - self.GIVEN_ARRAY_LEN % 4
        self.A = self.__get_defined_memory_distribution()
        print("THE VIRTUAL ADDRESS STREAM AS FOLLOWS:")
        for i in range(0, self.GIVEN_ARRAY_LEN, 4):
            print("a[{i_1}]={a_1}\t\ta[{i_2}]={a_2}\t\ta[{i_3}]={a_3}\t\ta[{i_4}]={a_4}"
                .format(
                i_1=i, i_2=i + 1, i_3=i + 2, i_4=i + 3,
                a_1=self.A[i], a_2=self.A[i + 1], a_3=self.A[i + 2], a_4=self.A[i + 3]
            ))

    def show_page_size_and_alg(self, input_alg, input_page_size):
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        self.__get_eliminate_Alg_from_arg(input_alg)
        self.update_PAGE_SIZE(input_page_size)
        print("PAGE NUMBER WITH SIZE {}k FOR EACH ADDRESS IS:".format(self.PAGE_SIZE // 1024))
        self.PAGE = self.__get_defined_page_distribution()
        for i in range(0, self.GIVEN_ARRAY_LEN, 4):
            print("page[{i_1}]={a_1}\t\tpage[{i_2}]={a_2}\t\tpage[{i_3}]={a_3}\t\tpage[{i_4}]={a_4}"
                .format(
                i_1=i, i_2=i + 1, i_3=i + 2, i_4=i + 3,
                a_1=self.PAGE[i], a_2=self.PAGE[i + 1], a_3=self.PAGE[i + 2], a_4=self.PAGE[i + 3]
            ))
        print("vmsize = {vmsize}k \t\t pagesize = {pagesize}k".format(vmsize=self.VIRTUAL_MEMORY_SIZE // 1024,
                                                                      pagesize=self.PAGE_SIZE // 1024))

    def change_page_size_and_alg(self, input_alg, input_page_size):
        self.__get_eliminate_Alg_from_arg(input_alg)
        self.update_PAGE_SIZE(input_page_size)
        print("PAGE NUMBER WITH SIZE {}k FOR EACH ADDRESS IS:".format(self.PAGE_SIZE // 1024))
        self.PAGE = self.__get_defined_page_distribution()
        print("vmsize = {vmsize}k \t\t pagesize = {pagesize}k".format(vmsize=self.VIRTUAL_MEMORY_SIZE // 1024,
                                                                      pagesize=self.PAGE_SIZE // 1024))

    def run_alg(self):
        print("------------- --------------"
              "\npage assigned pages_in/total references")
        for i in range(4, 33, 2):
            self.update_assign(i)
            if self.eliminate_Alg == 'lru'.lower():
                print("{}\t\t\t\t{}".format(self.assign, self.__lruAlg()))
            elif self.eliminate_Alg == 'opt'.lower():
                print("{}\t\t\t\t{}".format(self.assign, self.__optAlg()))
            elif self.eliminate_Alg == 'fifo'.lower():
                print("{}\t\t\t\t{}".format(self.assign, self.__fifoAlg()))
            elif self.eliminate_Alg == 'clock'.lower():
                print("{}\t\t\t\t{}".format(self.assign, self.__clockAlg()))

    def __get_defined_memory_distribution(self):
        a = [0] * self.GIVEN_ARRAY_LEN
        fifty_percentage_code_location = self.__get_random_memory_block()
        bias = 0
        for i in range(0, self.GIVEN_ARRAY_LEN // 2):
            bias = i * random.randint(4, 16) // 2
            a[i] = fifty_percentage_code_location + bias
        for i in range(self.GIVEN_ARRAY_LEN // 2, self.GIVEN_ARRAY_LEN // 2 + self.GIVEN_ARRAY_LEN // 4):
            a[i] = random.randint(0, fifty_percentage_code_location)

        for i in range(self.GIVEN_ARRAY_LEN // 4 * 3, self.GIVEN_ARRAY_LEN):
            a[i] = random.randint(fifty_percentage_code_location + bias, self.VIRTUAL_MEMORY_SIZE)
        return a

    def __get_defined_page_distribution(self):
        page = [0] * self.GIVEN_ARRAY_LEN
        for i in range(0, self.A.__len__()):
            page[i] = self.A[i] // self.PAGE_SIZE + 1
        return page

    def __get_random_memory_block(self):
        return random.randint(self.VIRTUAL_MEMORY_SIZE * 0.2 // 1,
                              self.VIRTUAL_MEMORY_SIZE * 0.8 // 1 - self.GIVEN_ARRAY_LEN)

    def __get_eliminate_Alg_from_input(self):
        alg = input("The algorithm is:")
        self.eliminate_Alg = alg.strip().lower()

    def __get_eliminate_Alg_from_arg(self, arg):
        print("The algorithm is:", end='\t')
        self.eliminate_Alg = arg.lower()
        print("{}".format(self.eliminate_Alg))

    def __optAlg(self):
        '''
(1） 最佳淘汰算法(OPT)。
这是一种理想的算法，可用来作为衡量其他算法优劣的依据，在实际系统中是难以实现的，因为它必须先知道指令
的全部地址流。由于本示例中已预先生成了全部的指令地址流，故可计算出最佳命中率。
该算法的准则是淘汰已满页表中不再访问或是最迟访问的的页。这就要求将页表中的页逐个与后继指令访问的所有
页比较，如后继指令不在访问该页，则把此页淘汰，不然得找出后继指令中最迟访问的页面淘汰。可见最佳淘汰算
法要花费较长的运算时间。
        :return:
        '''
        Queue = [None] * self.assign
        missing_page_count = 0
        tmp = 0
        current_p = 0
        current_Queue = None
        for i in self.PAGE:
            if i in Queue:
                pass
            else:
                if Queue.count(None) != 0:
                    Queue = self.__int2list(i) + Queue
                    Queue.pop(-1)
                    missing_page_count += 1
                else:
                    tmp = self.__predict(Queue.copy(), current_p)
                    # print("\t[*] POP PAGE {}".format(tmp))
                    Queue.pop(Queue.index(tmp))
                    Queue = self.__int2list(i) + Queue
                    missing_page_count += 1
            # print(Queue)
            current_p += 1
        # print(missing_page_count)
        return (missing_page_count + 0.0) / self.PAGE.__len__()

    def __predict(self, current_queue=None, current_pointer=0):
        '''
        选择永远不再需要的页面或最长时间以后才需要访问的页面予以淘汰
        预测规则：
            预测至少 assign - 1 个页面
        :return:
        '''
        value = -1
        for i in self.PAGE[current_pointer::]:
            if current_queue.__len__() == 1:
                return current_queue[0]
            else:
                if i in current_queue:
                    current_queue.remove(i)
                    continue
        return current_queue[-1]

    def __int2list(self, int_value):
        tmp = [0]
        tmp[0] = int_value
        return tmp

    def __lruAlg(self):
        '''
（2） 最近最少使用页淘汰算法(LRU)。
这是一种经常使用的方法，有各种不同的实施方案，这里采用的是不断调整页表链的方法，即总是淘汰页表链链首
的页，而把新访问的页插入链尾。如果当前调用页已在页表内，则把它再次调整到链尾。这样就能保证最近使用的
页，总是处于靠近链尾部分，而不常使用的页就移到链首，逐个被淘汰，在页表较大时，调整页表链的代价也是不
小的
        :return: 缺页率
        '''
        Queue = [None] * self.assign
        missing_page_count = 0
        tmp = 0
        for i in self.PAGE:
            if i in Queue:
                tmp = Queue.pop(Queue.index(i))
                Queue = self.__int2list(tmp) + Queue
            else:
                if Queue.count(None) != 0:
                    Queue = self.__int2list(i) + Queue
                    Queue.pop(-1)
                    missing_page_count += 1
                else:
                    # print("\t[*] POP PAGE {}".format(Queue[-1]))
                    Queue.pop(-1)
                    Queue = self.__int2list(i) + Queue
                    missing_page_count += 1
            # print(Queue)
        # print(missing_page_count)
        return (missing_page_count + 0.0) / self.PAGE.__len__()

    def __clockAlg(self):
        '''

        :return: 缺页率
        '''
        Queue = [None] * self.assign
        request = [0] * self.assign
        pointer = 0
        missing_page_count = 0
        for i in self.PAGE:
            if i in Queue:
                # 如果在队列中，则将 该值对应的访问位置为 1
                request[Queue.index(i)] = 1
            else:
                if Queue.count(None) != 0:
                    Queue[pointer] = i
                    request[pointer] = 1
                    pointer = (pointer + 1) % self.assign
                    missing_page_count += 1
                else:
                    # 如果不在队列中，发生缺页，首先将访问位表循环置 0 ，直到找到一个访问位为 0 的位置
                    while request[pointer] == 1:
                        request[pointer] = 0
                        pointer = (pointer + 1) % self.assign
                    # print("\t[*] POP PAGE {}".format(Queue[pointer]))
                    Queue[pointer] = i
                    # 将这个位置下的帧换下，换上调上来得页面，将访问位置 1 并将指针下移
                    request[pointer] = 1
                    missing_page_count += 1
                    pointer = (pointer + 1) % self.assign
            # print("request{} pointer{}".format(request,pointer))
            # print(Queue)
        return (missing_page_count + 0.0) / self.PAGE.__len__()

    def __fifoAlg(self):
        '''
FIFO 算法
        :return: 缺页率
        '''
        Queue = [None] * self.assign
        missing_page_count = 0
        tmp = 0
        current_Queue = None
        for i in self.PAGE:
            if i in Queue:
                pass
            else:
                if Queue.count(None) != 0:
                    Queue = self.__int2list(i) + Queue
                    Queue.pop(-1)
                    missing_page_count += 1
                else:
                    # print("\t[*] POP PAGE {}".format(Queue[-1]))
                    Queue.pop(-1)
                    Queue = self.__int2list(i) + Queue
                    missing_page_count += 1
            # print(Queue)
        return (missing_page_count + 0.0) / self.PAGE.__len__()

    def run_with_example1(self):
        '''
        LRU
        缺页率 :: 0.8333333333333334
        缺页率 :: 0.6666666666666666
        :return: None
        '''
        self.PAGE = [4, 3, 2, 1, 4, 3, 5, 4, 3, 2, 1, 5]
        # 例子来源于书第13题
        # print(self.PAGE)
        self.update_assign(3)
        print("缺页率 :: {}".format(self.__lruAlg()))
        self.update_assign(4)
        print("缺页率 :: {}".format(self.__lruAlg()))
        self.PAGE = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
        # 例子来自于网上
        self.update_assign(3)
        print("缺页率 :: {}".format(self.__optAlg()))
        self.update_assign(4)
        print("缺页率 :: {}".format(self.__optAlg()))
        self.PAGE = [3, 4, 2, 6, 4, 3, 7, 4, 3, 6, 3, 4, 8, 4, 6]
        # 例子来自 天勤 的书
        self.update_assign(3)
        print("缺页率 :: {}".format(self.__fifoAlg()))
        self.update_assign(3)
        print("缺页率 :: {}".format(self.__clockAlg()))


def start_main(alg):
    i = 1
    M = MemoryBlock()
    # M.update_VIRTUAL_MEMORY_SIZE(2 ** 20)
    M.init_with_random_num()
    M.show_page_size_and_alg(alg, 1024 * i)
    M.run_alg()
    for i in range(1, 9):
        M.change_page_size_and_alg(alg, 1024 * i)
        M.run_alg()


def start_main_with_image(alg):
    pass


def start_test():
    M = MemoryBlock()
    M.run_with_example1()


if __name__ == '__main__':
    # start_test()
    for alg in ['fifo', 'opt', 'lru', 'clock']:
        start_main(alg)
    # print(MemoryBlock().A)
