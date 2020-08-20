#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def fact(n):
    """
    递归方法计算阶乘
    """
    if n < 2:
        return 1
    
    return n * fact(n - 1)


if __name__ == "__main__":
    print(fact(0))
    print(fact(1))
    print(fact(5))
