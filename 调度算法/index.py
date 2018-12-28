import requests
import numpy as np


class PCB(object):
    def __init__(self, ID=0, PRIORITY=0, CPUTIME=0, ALLTIME=0, STATE='W', NEXT=0, FORWARD=0):
        self.ID = ID
        self.PRIORITY = PRIORITY
        self.CPUTIME = CPUTIME
        self.ALLTIME = ALLTIME
        self.STATE = STATE  # 进程状态
        self.NEXT = NEXT
        self.FORWARD = FORWARD


class PCBChain(object):
    def __init__(self):
        self.RUN = None
        self.HEAD = None
        self.TAIL = None
        self.Chain = []
        self.current_alg = None
        self.__verify = PCB()
        self.WAITING_QUEUE = []
        self.FINISH = False

    # def __gen_header(self,pcb1,pcb2):
    #     pcb1.FOWARD = None
    #     pcb1.NEXT = pcb2
    #     pcb2.FORWARD = pcb1
    #     self.HEAD= pcb1

    # def connect(self,pcb1,pcb2):
    #     CURRENT_NODE = self.HEAD
    #     if self.HEAD is None:
    #         self.__gen_header(pcb1,pcb2)
    #         return 1
    #     else:
    #         while CURRENT_NODE is None:
    #             CURRENT_NODE=CURRENT_NODE.NEXT
    #         CURRENT_NODE.NEXT =

    def append(self, pcb):
        '''
        后来觉得写的有问题，就优先级用了顺序表的方法，时间片用了链表的方法
        :param pcb:
        :return:
        '''
        if pcb.__class__ == self.__verify.__class__:
            self.Chain.append(pcb)
        else:
            print("type error")

    def ChangeAlg(self, alg):
        # print(self.Chain)
        if self.Chain != []:
            if alg in ["priority", "round robin"]:
                self.current_alg = alg
            else:
                print("type error")
        else:
            print("Append first")

    def prepare(self):
        # print(self.current_alg)
        if self.current_alg == "priority":
            self._order_by_priority()
            # 设置初始指针
            # self.RUN = self.Chain[0]
            # self.HEAD = self.Chain[1]
            # self.TAIL = self.Chain[-1]
        self.Chain[-1].NEXT = None
        for i in range(self.Chain.__len__() - 1):
            self.Chain[i].NEXT = self.Chain[i + 1]

        self.Chain[0].STATE = "R"

    def running(self):
        print("RUNNING PROC    WATING QUEUE")
        print("{}                {}".format("".join([str(word.ID) + " " for word in self.Chain])[:2],
                                            "".join([str(word.ID) + " " for word in self.Chain])[2:]))
        print("============================")
        print("ID                {}".format("".join([str(word.ID) + " " for word in self.Chain])))
        print("PRIORITY          {}".format("".join([str(word.PRIORITY) + " " for word in self.Chain])))
        print("CPUTIME           {}".format("".join([str(word.CPUTIME) + " " for word in self.Chain])))
        print("ALLTIME           {}".format("".join([str(word.ALLTIME) + " " for word in self.Chain])))
        print("STATE             {}".format("".join([str(word.STATE) + " " for word in self.Chain])))
        # print("NEXT              {}".format("".join([str(word.NEXT.ID) + " " for word in self.Chain if word.NEXT != None])) + "0")

        if self.current_alg == "priority":
            self.__priority_running()

        elif self.current_alg == "Round Robin".lower():
            self.__round_robin_running()

        if self.Chain == []:
            self.FINISH = True

        print("============================")

    def __priority_running(self):
        # 时间片到了
        self.Chain[0].STATE = "R"
        self.Chain[0].ALLTIME -= 1
        self.Chain[0].PRIORITY -= 3
        if self.Chain[0].ALLTIME <= 0:
            self.Chain.remove(self.Chain[0])
            if self.Chain.__len__() >= 1:
                self.Chain[0].STATE = "R"
            return
        if self.Chain.__len__() >= 2 and self.Chain[0].PRIORITY < self.Chain[1].PRIORITY:
            self.Chain[0].STATE = 'W'
            self.Chain[1], self.Chain[0] = self.Chain[0], self.Chain[1]
            self.Chain[0].STATE = 'R'
            return
        return

    def __round_robin_running(self):
        # 时间片到了
        self.Chain[0].STATE = "W"
        self.Chain[0].CPUTIME += 1
        self.Chain[0].ALLTIME -= 1
        # self.Chain
        if self.Chain != [] and self.Chain[0].ALLTIME <= 0:
            self.Chain.remove(self.Chain[0])
        if self.Chain != []:
            self.Chain.append(self.Chain.pop(0))
            self.Chain[0].STATE = "R"
        return

    def _order_by_priority(self):
        # 愚蠢的冒泡排序
        for j in range(0, self.Chain.__len__() - 1):
            c = 0
            for i in range(0, self.Chain.__len__() - 1 - j):
                if self.Chain[i].PRIORITY < self.Chain[i + 1].PRIORITY:
                    self.Chain[i], self.Chain[i + 1] = self.Chain[i + 1], self.Chain[i]
                    c += 1
                if c == 0:
                    break


# class TestAlg():
#     def __init__(self, matirx):
#         '''
#         matrix is a mat with
#         :param matirx:
#         '''
#         try:
#             np.array()



def testing_mode_1():
    # print("TYPE THE ALGORITHM:")
    pcb1 = PCB(ID=1, PRIORITY=9, ALLTIME=3)
    pcb2 = PCB(ID=2, PRIORITY=41, ALLTIME=4)
    pcb3 = PCB(ID=3, PRIORITY=30, ALLTIME=6)
    pcb4 = PCB(ID=4, PRIORITY=29, ALLTIME=3)
    pcb5 = PCB(ID=5, PRIORITY=0, ALLTIME=4)
    alg = input("TYPE THE ALGORITHM:").lower()
    # elif self.current_alg == "Round Robin".lower():
    pcb_chain = PCBChain()
    pcb_chain.append(pcb1)
    pcb_chain.append(pcb2)
    pcb_chain.append(pcb3)
    pcb_chain.append(pcb4)
    pcb_chain.append(pcb5)
    # alg = "Round Robin".lower()
    # alg = "priority"
    if alg == "priority".lower():
        print("====================")
        pcb_chain.ChangeAlg(alg)
        pcb_chain.prepare()
        while pcb_chain.FINISH == False:
            pcb_chain.running()
        # print(pcb_chain.current_alg)
    elif alg == "Round Robin".lower():
        print("====================")
        pcb_chain.ChangeAlg(alg)
        pcb_chain.prepare()
        while pcb_chain.FINISH == False:
            pcb_chain.running()
    print("SYSTEM FINISH")


if __name__ == '__main__':
    testing_mode_1()
