# Linux 死锁概念与银行家算法


## 一 . 死锁的概念

在之前的哲学家吃饭的问题中，当每个哲学家都想进餐的时候，他们都会占用左手边的筷子。当他们想要拿起右手边的筷子的时候，因为没有资源了。所以程序会进入无线等待的状态，这就是死锁。

我们可以来想想一个更加简单的例子。比如说有两个信号量集，一个是扫描机，一个是打印机。P1程序占用打印机，P2程序占用扫描机。当P1程序在运行的时候想要获取扫描机的信号量，同时P2程序想要在运行的时候获取打印机的信号量的时候。就会发生死锁。

概括而言。我们可以发现死锁的会有如下共性：

- 参与死锁的进程至少有两个
- 每个参与死锁的进程都要等待资源
- 参与死锁的进程中至少有两个进程占用资源

可见，死锁之所以产生，是因为每个进程都要竞争资源。由于**系统资源不足，并且推进程序不当**，因此产生了死锁

## 二 . 死锁实例演示

在之前的消费者和生产者问题中，如果改变了 生产者的 信号量处理方法，则会产生死锁。具体实例如下所示，代码参考 `producer_and_consumer-dead-lock.c`

![image_1coqff5k4kvr5h3b156vtg6r9.png-203.3kB][1]

直接运行程序，可以发现程序是直接卡死的。这里的解决办法就是Provider 下方的`usleep(1000)`。让消费者先行一步。即可避免死锁。

## 三 . 银行家算法
> 鄙人C语言编程能力有限，不知道如何将银行家算法的问题和具体操作系统中的实际死锁避免问题联系起来。
只给出一个python版本的矩阵操作来模拟银行家算法。
翻了翻谷歌，看到一篇前辈写的银行家算法c实现，也同样是模拟而不是和实际问题相互结合具体可以看看：[银行家算法（C语言实现）][2]

银行家算法是DJ提出的，最具代表性的避免死锁算法。假设系统中有 n个进程 P1-Pn 和 m类资源 R1-Rm，那么建立以下形式的数据结构：

### 银行家算法的数据结构

- 可用资源向量 Available 长度为 m 。代表所有资源 A[i] 表示第i+1类资源现有的资源数量。
- 最大需求矩阵 Max 。n * m 的矩阵。定义每个进程对 m 类资源的最大需求数。 比如 M[i][j] 表示第 i 个进程最多需要的 m 类资源的数目。
- 分配矩阵 Allocation 。 n * m 的矩阵。定义每个进程**已经分配**的资源数目。
- 需求矩阵 Need 。 n * m 的矩阵。定义每个进程**还需分配**的资源数目。
- 请求向量 $request_i$ 。长度未 m 的向量。代表单次某进程请求的资源量

对此，有关系如下:
$$ Need[i][j] = Max[i][j] - Available[i][j] $$

### 银行家算法的算法描述

- 发出请求向量 $request_i$ 
- 判断 $request_i$ 是否小于等于 $need_i$ 否则报错（需要的东西太多了！）
- 判断 $request_i$ 是否小于等于 $available_i$ 否则等待  （资源不够用）
- 先对所有的资源进行预分配，修改为如下的值：
    - $Allocation_i = Allocation_i + Request_i$
    - $Available = Available -Request_i$
    - $Need_i = Need_i - Request_i$
- 之后对修改的向量进行安全性算法。安全则修改，不安全则回退之前的状态

### 安全性算法

- 建立 Work[m] 和 Finish[n]。初始化如下
    - $Work = Available; Finish = [False] * n$
- 查找 i 满足如下条件
    - $Finish[i] = false ; Need_i <= Work$
    - 满足则执行 $Work = Work + Allocation_i ; Finish[n] = True$
- 注意这里是查找，而不是顺序执行。
- 如果Finish都是True。则允许修改。

### 银行家算法 py 实现

**定义数据结构**
```python
    def __init__(self, n=4, m=3):
        self.n = n  # 进程数量
        self.m = m  # 资源有多少类

        self.Available = []  # 可用资源向量

        self.Max = {}  # 最大需求矩阵
        for i in range(0, self.n):
            self.Max["P{}".format(i)] = []
        self.Allocation = {}  # 分配矩阵
        for i in range(0, self.n):
            self.Allocation["P{}".format(i)] = []
        self.Need = {}  # 需求矩阵
        for i in range(0, self.n):
            self.Need["P{}".format(i)] = []
        self.Request = {}
        for i in range(0, self.n):
            self.Request["P{}".format(i)] = []
```

**请求部分**
```python
    def sendRequest(self, Px, vector):
        '''
        :param Px: 字符串...P0-P4
        :param vector: 请求向量，为一个列表
        :return:
        '''
        self.checkRequestInputValid()
        self.Request[Px] = vector
        print(self.Request)
        for i in range(0, self.m):
            if self.Request[Px][i] > self.Need[Px][i]:
                raise CommonError("{}申请的资源数目Available[{}]不应该超过它的需求数目".format(Px, i))
            if self.Request[Px][i] > self.Available[i]:
                raise CommonError("{}需要等待，因为目前可用资源 Available[{}] 不够".format(Px, i))

        tmp_Available = self.Available
        tmp_Allocation = self.Allocation
        tmp_Need = self.Need

        for i in range(0, self.m):
            tmp_Available[i] = tmp_Available[i] - self.Request[Px][i]
            tmp_Allocation[Px][i] = tmp_Allocation[Px][i] + self.Request[Px][i]
            tmp_Need[Px][i] = tmp_Need[Px][i] - self.Request[Px][i]

        if self.checkTmpMatrixSafe(tmp_Available, tmp_Allocation, tmp_Need) is True:
            print("[+] Check safe ; Format changed")
            self.Allocation = tmp_Allocation
            self.Available = tmp_Available
            self.Need = tmp_Need
```

**安全性校验**

```python
# 这里的查找不是很好实现。我的做法是找到一个可用的之后回退，再找一次前面的，方法比较low。可能思路有些不太对。不知道操作系统里是如何实现的

    def checkTmpMatrixSafe(self, tmp_Available, tmp_Allocation, tmp_Need):
        Work = tmp_Available
        Finish = [False] * self.n

        # finding valid i

        def helperChecker(tmp_Need_Px, Work, m):
            tag = True
            for i in range(0, m):
                if tmp_Need_Px[i] > Work[i]:
                    tag = False
            return tag

        for i in range(0, self.n):
            if Finish[i] is True:
                continue
            if Finish[i] is False and helperChecker(tmp_Need["P{}".format(i)], Work, self.m):
                print("[*] Finding P{} safe".format(i))
                for j in range(0, self.m):
                    Work[j] = Work[j] + tmp_Allocation["P{}".format(i)][j]
                Finish[i] = True
                print(Work)
# ... #
                「将上述操作重复一边，范围是 (0,i) 感觉这里有可以优化的地方」
# ... #
        if Finish == [True] * self.n:
            # tmp_Available = __tmp_Available
            return True
        else:
            return False
```
**样例**
按照书上的写了个两个样例。运行通过～
```python
        self.Available = [1, 1, 2]
        self.Max = {
            "P0": [3, 2, 2],
            "P1": [6, 1, 3],
            "P2": [3, 1, 4],
            "P3": [4, 2, 2]
        }
        self.Allocation = {
            "P0": [1, 0, 0],
            "P1": [5, 1, 1],
            "P2": [2, 1, 1],
            "P3": [0, 0, 2]
        }
        self.getNeed()

def example1():
    try:
        Bancker = BankerAlgorithm()
        Bancker.exampleInit1()
        Bancker.sendRequest("P1", [1, 0, 1])
    except Exception as e:
        print(e)

{'P2': [], 'P1': [1, 0, 1], 'P0': [], 'P3': []}
[*] Finding P1 safe
[6, 2, 3]
[*] Finding P0 safe
[1, 0, 0] 0
[7, 2, 3]
[*] Finding P2 safe
[9, 3, 4]
[*] Finding P3 safe
[9, 3, 6]
[+] Check safe ; Format changed
```

### 下载地址

[http://shaobaobaoer.cn/cdn/bancker.zip][3]



    


  [1]: http://static.zybuluo.com/shaobaobaoer/9kzoll4ne9hk4xgx04kxen6b/image_1coqff5k4kvr5h3b156vtg6r9.png
  [2]: http://baoxizhao.com/2017/06/04/%E9%93%B6%E8%A1%8C%E5%AE%B6%E7%AE%97%E6%B3%95%EF%BC%88C%E8%AF%AD%E8%A8%80%E5%AE%9E%E7%8E%B0%EF%BC%89/
  [3]: http://shaobaobaoer.cn/cdn/bancker.zip