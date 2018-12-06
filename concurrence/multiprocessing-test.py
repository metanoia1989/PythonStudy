#!/usr/bin/env python3
# -*- coding: utf-8  -*-

from multiprocessing import Pool
import time 

COUNT = 50000000
def countdown(n):
    while n > 0:
        n -= 1
    
if __name__ == "__main__":
    pool = Pool(processes=2)
    start_time = time.time()
    r1 = pool.apply_async(countdown, [COUNT//2])
    r2 = pool.apply_async(countdown, [COUNT//2])
    pool.close()
    pool.join()
    end_time = time.time()
    print("线程运行 {} 秒".format(end_time - start_time))