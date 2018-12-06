#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import threading 
import time


class newThread(threading.Thread):
    """继承 threading.Thread 线程类，重写 __init__ 和 run 方法来创建线程 """
    def __init__(self, threadID, name, counter):
        super().__init__()
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        """
        获得锁，成功锁定后返回True
        可选的timeout参数不填时将一直阻塞知道获得锁定
        否则超市后将返回false
        """
        print("线程开始运行 {}".format(self.name))
        threadLock.acquire()
        print_time(self.name, self.counter, len(list0))
        # 释放锁
        threadLock.release()
    
    def __del__(self):
        print("{} 线程结束".format(self.name))

def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        list0[counter-1] += 1
        print("[{0}] {1} 修改第 {2}个值，修改后值为: {3}".format(time.ctime(time.time()), threadName, counter, list0[counter-1]))
        counter -= 1

print("主线程开始执行")

list0 = [ 0 ] * 12
threadLock = threading.Lock()
threads = []

# 创建新线程
thread1 = newThread(1, "线程-1", 1)
thread2 = newThread(2, "线程-2", 2)

# 启动线程
thread1.start()
thread2.start()

# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)

# 阻塞直所有线程完成
for t in threads:
    t.join()

print("主线程结束")