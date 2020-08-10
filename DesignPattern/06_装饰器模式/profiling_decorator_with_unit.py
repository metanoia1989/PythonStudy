#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
打印时间为毫秒或秒的斐波那契代码
"""

import time
from functools import wraps

def profiling_decorator_with_unit(unit):
    def profiling_decorator(f):
        @wraps(f)
        def wrap_f(n):
            start_time = time.time()
            result = f(n)
            end_time = time.time()
            if unit == "seconds":
                elapsed_time = (end_time - start_time) / 1000
            else:
                elapsed_time = (end_time - start_time)

            print("[Time elapsed for n = {}] {}".format(n, elapsed_time))
            return result

        return wrap_f
    return profiling_decorator

@profiling_decorator_with_unit('seconds')
def fib(n):
    if n < 2:
        return

    fibPrev = 1
    fib = 1

    for num in range(2, n):
        fibPrev, fib = fib, fib + fibPrev
    
    return fib

if __name__ == "__main__":
    n = 77
    print("Fibonacci number for n = {}: {}".format(n, fib(n)))