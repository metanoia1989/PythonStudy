#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

def fib_cached(n, cache):
    if n < 2:
        return 1
    
    if n in cache:
        return cache[n]

    cache[n] = fib_cached(n - 2, cache) + fib_cached(n - 1, cache)

if __name__ == "__main__":
    cache = {}
    start_time = time.time()
    fib_sequence = [fib_cached(x, cache) for x in range(0, 10)]
    end_time = time.time()

    print(
        "Calculating the list of {} Fibonacci numbers took {} seconds"
        .format(
            len(fib_sequence),
            end_time - start_time
        )
    )