#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
缓存函数结果
这个是没缓存版的，直接爆了
"""

import time

def fib(n):
    if n < 2:
        return 1

    return fib(n - 2) + fib(n - 1)

if __name__ == "__main__":
    start_time = time.time()
    fib_sequence = [fib(x) for x in range(1, 80)]
    end_time = time.time()

    print(
        "Calculating the list of {} Fibonacci numbers took {} seconds"
        .format(
            len(fib_sequence),
            end_time - start_time
        )
    )