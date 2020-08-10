#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建性能测量函数
"""

import time

def fib(n):
    if n < 2:
        return

    fibPrev = 1
    fib = 1

    for num in range(2, n):
        fibPrev, fib = fib, fib + fibPrev
    
    return fib

def profile_me(f, n):
    start_time = time.time()
    result = f(n)
    end_time = time.time()
    print("[Time elapsed for n = {}] {}".format(n, end_time - start_time))
    return result

if __name__ == "__main__":
    n = 77
    print("Fibonacci number for n = {}: {}".format(n, profile_me(fib, n)))