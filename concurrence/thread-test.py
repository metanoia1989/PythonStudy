#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import _thread as thread
import time

# 定义一个线程要执行的函数
def print_time( threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print("{}: {}".format(threadName, time.ctime(time.time())))
    
# 创建两个线程
try:
    thread.start_new_thread(print_time, ("线程1", 2, ))
    thread.start_new_thread(print_time, ("线程2", 4, ))
except Exception as e:
    print("Error: 无法启动线程")
    raise e


while True:
    pass