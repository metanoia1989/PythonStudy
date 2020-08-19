#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
利用函数实现策略模式
"""

def executor(arg1, arg2, func=None):
    if func is None:
        print("Strategy not implementd ...")
    else:
        func(arg1, arg2)

def strategy_addition(arg1, arg2):
    print(arg1 + arg2)

def strategy_subtraction(arg1, arg2):
    print(arg1 - arg2)

if __name__ == "__main__":
    executor(4, 6)
    executor(4, 6, strategy_addition)
    executor(4, 6, strategy_subtraction)