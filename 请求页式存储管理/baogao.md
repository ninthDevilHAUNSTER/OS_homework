# 操作系统实验报告 - 请求页面存储管理

标签（空格分隔）： 操作系统

---

## 一、实验目的与要求

### 1.1 目的
近年来，由于大规模集成电路（LSI）和超大规模集成电路（VLSI）技术的发展，使存储器的容量不断扩大，
价格大幅度下降。但从使用角度看，存储器的容量和成本总受到一定的限制。所以，提高存储器的效率始终是操作系统研究的重要课题之一。虚拟存储技术是用来扩大内存容量的一种重要方法。学生应独立地用高级语言编写几个常用的存储分配算法，并设计一个存储管理的模拟程序，对各种算法进行分析比较，评测其性能优劣，从而加深对这些算法的了解。
### 1.2 要求
为了比较真实地模拟存储管理，可预先生成一个大致符合实际情况的指令地址流。然后模拟这样一种指令序列
的执行来计算和分析各种算法的访问命中率。
### 1.3 实验描述
本示例是采用页式分配存储管理方案，并通过分析计算不同页面淘汰算法情况下的访问命中率来比较各种
算法的优劣。另外也考虑到改变页面大小和实际存储器容量对计算结果的影响，从而可为算则好的算法、合适的页面尺寸和实存容量提供依据。

示例中选用最佳淘汰算法（OPT）和最近最少使用页面淘汰算法（LRU）计算页面命中率。公式为
$$命中率  = 1- \cfrac {页面失效次数}{页面地址长度}$$
假定虚存容量为 32K，页面尺寸从 1K 至 8K，实存容量从 4 页至 32 页。

## 二、实验环境

- Windows 10 64位
- Python 3.6

## 三、实验内容及其设计与实现

### 3.0 实验的数据结构说明

为了完成该实验的各项指标，设定若干数据结构，说明如下

```python
class MemoryBlock(object):
    def __init__(self):
        self.VIRTUAL_MEMORY_SIZE = 32 * 2 ** 10
        self.PAGE_SIZE = 1024
        self.GIVEN_ARRAY_LEN = 256
#        self.size = 1
        self.assign = 4
        self.A = []
        self.PAGE = []
        self.eliminate_Alg = None
        self.RESULT_MAT = {}
        self.__color_map = ['r', 'b', 'y', 'g', 'darkblue', 'darkred', 'orange', 'purple', 'brown', 'pink']

```

- `self.VIRTUAL_MEMORY_SIZE` 内存大小
- `self.PAGE_SIZE` 页面大小
- `self.GIVEN_ARRAY_LEN` 给出的指令流长度
- `self.assign` 页框大小
- `self.A` 内存存放的列表，Index为指令号，值为内存地址
- `self.PAGE` 页面号的列表，Index为页面号,值为页面地址
- `self.eliminate_Alg` 淘汰算法
- `self.RESULT_MAT` 存放结果
- `self.__color_map` 画图时候的调色盘


### 3.1 初始化内存序列与页面序列

**3.1.1 生成序列要求**

本程序是按下述原则生成指令序列的：

- （1） 50%的指令是顺序执行的。
- （2） 25%的指令均匀散布在前地址部分。
- （3） 25%的指令均匀散布在后地址部分。

**3.1.2 内存序列生成**

利用random生成随机的地址序列。设置`fifty_percentage_code_location`来定位前50%的指令位置。将25% 指令生成在 `fifty_percentage_code_location`之前，25% 指令随机生成在 `fifty_percentage_code_location`之后。
```python
def init_with_random_num(self):
    self.GIVEN_ARRAY_LEN = int(input(">> PLEASE INPUT GIVEN_ARRAY_LEN")) // 1
    self.GIVEN_ARRAY_LEN = self.GIVEN_ARRAY_LEN - self.GIVEN_ARRAY_LEN % 4
    self.A = self.__get_defined_memory_distribution()
    self.PAGE = self.__get_defined_page_distribution()
    print("THE VIRTUAL ADDRESS STREAM AS FOLLOWS:")

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
```

**3.1.3 页面序列生成**

```python
def __get_defined_page_distribution(self):
    page = [0] * self.GIVEN_ARRAY_LEN
    for i in range(0, self.A.__len__()):
        page[i] = self.A[i] // self.PAGE_SIZE + 1
    return page
```

**3.1.4 结果正确性验证**

随机生成结果如下，红色为顺序分布，蓝色为前面的随机分布，绿色为后面的随机分布

![TIM图片20181228124557.png-54.4kB][1]

页面也是相同的样子。符合题目要求。

### 3.2 FIFO 算法与结果分析

**3.2.1 FIFO算法介绍**

置换最先调入内存的页面，即置换在内存中驻留时间最久的页面。按照进入内存的先后次序排列成队列，从队尾进入，从队首删除。但是该算法会淘汰经常访问的页面，不适应进程实际运行的规律，目前已经很少使用。

**3.2.2 代码分析**

由于python没有类似于队列或者栈的数据结构，需要自己定义一种特殊的出队入队方法。设置了`__int2list`方法，来让元素执行入队操作。利用pop方法来执行出队操作。

```python
    def __int2list(self, int_value):
        tmp = [0]
        tmp[0] = int_value
        return tmp
        
    def __fifoAlg(self):
        '''
FIFO 算法
        :return: 缺页率
        '''
        Queue = [None] * self.assign
        missing_page_count = 0
        for i in self.PAGE:
            if i in Queue:
                pass
            else:
                if Queue.count(None) != 0:
                    Queue = self.__int2list(i) + Queue
                    Queue.pop(-1)
                    missing_page_count += 1
                else:
                    Queue.pop(-1)
                    Queue = self.__int2list(i) + Queue
                    missing_page_count += 1
        return (missing_page_count + 0.0) / self.PAGE.__len__()
```
**3.2.3 算法可行性分析**

按照上图设置页面访问顺序，与手算完全一致，算法正确

```shell
    self.PAGE = [3, 4, 2, 6, 4, 3, 7, 4, 3, 6, 3, 4, 8, 4, 6]
    # 例子来自 天勤 的书
    self.update_assign(3)
    print("缺页率 :: {}".format(self.__fifoAlg()))
    
[3, None, None]
[4, 3, None]
[2, 4, 3]
	[*] POP PAGE 3
[6, 2, 4]
[6, 2, 4]
	[*] POP PAGE 4
[3, 6, 2]
	[*] POP PAGE 2
[7, 3, 6]
	[*] POP PAGE 6
[4, 7, 3]
[4, 7, 3]
	[*] POP PAGE 3
[6, 4, 7]
	[*] POP PAGE 7
[3, 6, 4]
[3, 6, 4]
	[*] POP PAGE 4
[8, 3, 6]
	[*] POP PAGE 6
[4, 8, 3]
	[*] POP PAGE 3
[6, 4, 8]
缺页率 :: 0.8
```

**3.2.4 图表分析**

![fifo plt with 8lines.png-39.8kB][2]


### 3.3 OPT 算法与结果分析

**3.3.1 OPT 算法**

这是一种理想的算法，可用来作为衡量其他算法优劣的依据，在实际系统中是难以实现的，因为它必须先知道指令的全部地址流。由于本示例中已预先生成了全部的指令地址流，故可计算出最佳命中率。

该算法的准则是淘汰已满页表中不再访问或是最迟访问的的页。这就要求将页表中的页逐个与后继指令访问的所有页比较，如后继指令不在访问该页，则把此页淘汰，不然得找出后继指令中最迟访问的页面淘汰。可见最佳淘汰算法要花费较长的运算时间。

**3.3.2 代码分析**

为了完成opt那种所谓的预测，需要写一个辅助函数`__predict`来完成相关的操作
```python

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
```
该算法预测了至少 assign-1个页面。如果后 $\{K | K ≥ assign-1\}$中，有存在于队列中的置换页号，则暂时将这个页号剔除，当队列长度为1的时候，当前队列里的唯一元素就是需要正真淘汰的页号。当然，在预测到快结束的时候，队列长度最后可能大于1，那么就返回当前暂存队列中的最后一个元素。

有了 预测函数后，就可以实现opt算法了
```python
    def __optAlg(self):
        '''
最佳淘汰算法(OPT)。
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
```

**3.3.3 算法可行性分析**

页面访问顺序为[2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]。其结果应该为如下

![TIM截图20181228131218.png-16.3kB][3]

实验结果如下，与手算结果完全一致
```python
[2, None, None]
[3, 2, None]
[3, 2, None]
[1, 3, 2]
	[*] POP PAGE 1
[5, 3, 2]
[5, 3, 2]
	[*] POP PAGE 2
[4, 5, 3]
[4, 5, 3]
[4, 5, 3]
	[*] POP PAGE 3
[2, 4, 5]
[2, 4, 5]
[2, 4, 5]
缺页率 :: 0.5
```

**3.3.4 图表分析**

![opt plt with 8lines.png-35.7kB][4]

### 3.4 LRU 算法与结果分析

**3.4.1 LRU 算法**
这是一种经常使用的方法，有各种不同的实施方案，这里采用的是不断调整页表链的方法，即总是淘汰页表链链首的页，而把新访问的页插入链尾。如果当前调用页已在页表内，则把它再次调整到链尾。这样就能保证最近使用的页，总是处于靠近链尾部分，而不常使用的页就移到链首，逐个被淘汰，在页表较大时，调整页表链的代价也是不小的

**3.4.2 代码分析**

算法还是比较简单的，在fifo基础上修改，如果查到了，那么就把查到的元素给放到最前面去即可。
```python
    def __lruAlg(self):
        '''
（2） 最近最少使用页淘汰算法(LRU)。
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
        return (missing_page_count + 0.0) / self.PAGE.__len__()
```

**3.4.3 可行性分析**

该题的样例来自于书第 13题。

```python
        self.PAGE = [4, 3, 2, 1, 4, 3, 5, 4, 3, 2, 1, 5]
        # 例子来源于书第13题
        self.update_assign(3)
        print("缺页率 :: {}".format(self.__lruAlg()))
        
[4, None, None]
[3, 4, None]
[2, 3, 4]
	[*] POP PAGE 4
[1, 2, 3]
	[*] POP PAGE 3
[4, 1, 2]
	[*] POP PAGE 2
[3, 4, 1]
	[*] POP PAGE 1
[5, 3, 4]
[4, 5, 3]
[3, 4, 5]
	[*] POP PAGE 5
[2, 3, 4]
	[*] POP PAGE 4
[1, 2, 3]
	[*] POP PAGE 3
[5, 1, 2]
缺页率 :: 0.8333333333333334
```
与手算结果完全一致，算法正确


**3.4.4 图表分析**

![lru plt with 8lines.png-40.1kB][5]

### 3.5 CLOCK 算法与结果分析

**3.5.1 CLOCK 算法**

钟替换算法（Clock）,给每个页帧关联一个使用位。当该页第一次装入内存或者被重新访问到时，将使用位置为1。每次需要替换时，查找使用位被置为0的第一个帧进行替换。在扫描过程中，如果碰到使用位为1的帧，将使用位置为0，在继续扫描。如果所谓帧的使用位都为0，则替换第一个帧。

**3.5.2 代码分析**

算法的注释就是代码分析
```python
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
```

**3.5.3 可行性分析**

按照上图设置页面访问顺序，与手算完全一致，算法正确

```python
        self.PAGE = [3, 4, 2, 6, 4, 3, 7, 4, 3, 6, 3, 4, 8, 4, 6]
        # 例子来自 天勤 的书
        self.update_assign(3)
        print("缺页率 :: {}".format(self.__clockAlg()))

[3, None, None]
[3, 4, None]
[3, 4, 2]
	[*] POP PAGE 3
[6, 4, 2]
[6, 4, 2]
	[*] POP PAGE 2
[6, 4, 3]
	[*] POP PAGE 4
[6, 7, 3]
	[*] POP PAGE 6
[4, 7, 3]
[4, 7, 3]
	[*] POP PAGE 7
[4, 6, 3]
[4, 6, 3]
[4, 6, 3]
	[*] POP PAGE 3
[4, 6, 8]
[4, 6, 8]
[4, 6, 8]
缺页率 :: 0.6
```

**3.5.4 图表分析**

![clock plt with 8lines.png-40.3kB][6]

### 3.6 图表制作

将数据以字典的方式存放到`RESULT_MAT`中，在draw_plot函数中读取它

RESULT_MAT是一个字典，键位 页面大小，值为一个二元列表，一元存放页框大小，一元存放缺页率

```python
        ...
            elif self.eliminate_Alg == 'clock'.lower():
                print("{}\t\t\t\t{}".format(self.assign, self.__clockAlg()))
                result_mat_mingzhonglv.append(self.__clockAlg())
        self.RESULT_MAT[self.PAGE_SIZE] = []
        self.RESULT_MAT[self.PAGE_SIZE].append(result_mat_assign)
        self.RESULT_MAT[self.PAGE_SIZE].append(result_mat_mingzhonglv)
```

之后，通过pyplot可以将图片画出来，并用save_data函数调用pickle包保存数据。

```python
    def draw_plot(self):
        print(self.RESULT_MAT)
        index = 1
        for key, value in self.RESULT_MAT.items():
            X, Y = self.RESULT_MAT[key][0], self.RESULT_MAT[key][1]
            plt.plot(X, Y, label='page_size {}K'.format(index), c=self.__color_map[index - 1])
            index += 1
        plt.legend()

        plt.xlabel("PAGE SIZE/K {} alg".format(self.eliminate_Alg))
        plt.ylabel("Que ye lv")
        plt.savefig('./img/{} plt with {}lines.png'.format(self.eliminate_Alg, index - 1))
        plt.show()
        self.save_data()
```

在之后的综合分析中，还要用到这些数据。来分析页面大小相同的时候，各种算法的优劣。在load_data_and_draw_plot.py中，有明确的代码,内容基本相似，主要代码如下：

```python
def load_data(page_size):
    ...
    opt_dict = pickle.load(open('./data/opt-data.txt', 'rb'))
    RESULT_MAT = {
        ...
        'opt': opt_dict[page_size]
    }
    draw_plot(RESULT_MAT, page_size)
def draw_plot(RESULT_MAT, page_size):
    index = 1
    for key, value in RESULT_MAT.items():
        X, Y = RESULT_MAT[key][0], RESULT_MAT[key][1]
        plt.plot(X, Y, label='{} alg analyze page_size {}K'.format(key, page_size // 1024), c=color_map[index - 1])
        index += 1
        ...
```

### 3.7 综合分析

分析四种算法，在页面尺寸为1K 的时候，可以发现，除了opt之前外，其他四种算法的缺页率基本相似。但opt算法明显低一些。

![4 alg analyze with page size 1.png-42.6kB][7]

随着页面尺寸增加，OPT算法的优势逐渐丧失。

![4 alg analyze with page size 2.png-36.8kB][8]
![4 alg analyze with page size 3.png-35.3kB][9]


## 四、收获与体会

说明：撰写本小组完成该实验后的收获和体会，各组员分别填写。


  [1]: http://static.zybuluo.com/shaobaobaoer/8dbuam8swgbma8a1khkg01qk/TIM%E5%9B%BE%E7%89%8720181228124557.png
  [2]: http://static.zybuluo.com/shaobaobaoer/ukh5f5r43299wwlclx4ib91y/fifo%20plt%20with%208lines.png
  [3]: http://static.zybuluo.com/shaobaobaoer/hwc49eeg526e76sj7euw2pbf/TIM%E6%88%AA%E5%9B%BE20181228131218.png
  [4]: http://static.zybuluo.com/shaobaobaoer/vb751wodllyttg1fatbg90o3/opt%20plt%20with%208lines.png
  [5]: http://static.zybuluo.com/shaobaobaoer/yvdfr8mbubh32s2fauxcbxsu/lru%20plt%20with%208lines.png
  [6]: http://static.zybuluo.com/shaobaobaoer/v5sjearoccuwb3xgwxv6whkz/clock%20plt%20with%208lines.png
  [7]: http://static.zybuluo.com/shaobaobaoer/0udzj3r47wnegrrm0ixefynr/4%20alg%20analyze%20with%20page%20size%201.png
  [8]: http://static.zybuluo.com/shaobaobaoer/7o9ez7xmrs3pg0kr41wjijdl/4%20alg%20analyze%20with%20page%20size%202.png
  [9]: http://static.zybuluo.com/shaobaobaoer/h637hw1fzujpclp7dq8eet2m/4%20alg%20analyze%20with%20page%20size%203.png