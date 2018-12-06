#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import threading
import time 
from queue import Queue 

exitFlag = 0

class newThread(threading.Thread):
    """继承 threading.Thread 线程类，重写 __init__ 和 run 方法来创建线程 """
    def __init__(self, threadID, name, queue):
        super().__init__()
        self.threadID = threadID
        self.name = name
        self.queue = queue

    def run(self):
        """ 线程的执行代码，线程创建后会直接运行run函数 """
        print("启动线程 {}".format(self.name))
        process_data(self.name, self.queue)
        print("退出线程 {}".format(self.name))

def process_data(threadName, queue):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = queue.get()
            queueLock.release()
            print("{} processing {}".format(threadName, data))
        else:
            queueLock.release()
        time.sleep(1)


print("主线程开始执行")
threadList = ["线程1", "线程2", "线程3"]
nameList = ["第一个", "第二个", "第三个", "第四个", "第五个"]
queueLock = threading.Lock()
workQueue = Queue(10)
threads = []
threadID = 1

# 创建新线程
for name in threadList:
    thread = newThread(threadID, name, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print("主线程结束")
