#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
创建 calculator 对象
"""

class Calculator(object):
    def fib_cached(self, n, cache):
        if n < 2:
            return 1
        
        if n in cache:
            return cache[n]

        cache[n] = fib_cached(n - 2, cache) + fib_cached(n - 1, cache)
        return cache[n]