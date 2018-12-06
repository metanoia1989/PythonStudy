#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import threading
import time 

exitFlag = 0

class newThread(threading.Thread):
    """继承 threading.Thread 线程类，重写 __init__ 和 run 方法来创建线程 """
    def __init__(self, threadID, name, counter):
        super().__init__()
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        """ 线程的执行代码，线程创建后会直接运行run函数 """
        print("启动线程 {}".format(self.name))
        print_time(self.name, self.counter, 5)
        print("退出线程 {}".format(self.name))

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            (threading.Thread).exit()
        time.sleep(delay)
        print("{}: {}".format(threadName, time.ctime(time.time())))
        counter -= 1

print("主线程开始执行")


# 创建新线程
thread1 = newThread(1, "线程-1", 1)
thread2 = newThread(2, "线程-2", 2)

# 启动线程
thread1.start()
thread2.start()

print("主线程结束")