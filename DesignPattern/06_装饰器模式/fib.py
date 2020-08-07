#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
斐波那契数列
"""

import time

n = 77

start_time = time.time()
fibPrev = 1
fib = 1

for num in range(2, n):
    fibPrev, fib = fib, fib + fibPrev

end_time = time.time()

print("[Time elapsed for n = {}] {}".format(n, end_time - start_time))
print("Fibonacci number for n = {}: {}".format(n, fibPrev))