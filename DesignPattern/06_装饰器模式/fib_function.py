#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

def fib(n):
    start_time = time.time()
    if n < 2:
        return

    fibPrev = 1
    fib = 1

    for num in range(2, n):
        fibPrev, fib = fib, fib + fibPrev

    end_time = time.time()
    print("[Time elapsed for n = {}] {}".format(n, end_time - start_time))

    return fib

if __name__ == "__main__":
    n = 77    
    print("Fibonacci number for n = {}: {}".format(n, fib(n)))

