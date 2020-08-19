#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用 if...else 的加法和减法策略
"""


def reducer(arg1, arg2, strategy=None):
    if strategy == "addition":
        print(arg1 + arg2)
    elif strategy == "subtraction":
        print(arg1 - arg2)
    else:
        print("Strategy not implemented...")

if __name__ == "__main__":
    reducer(4, 6)
    reducer(4, 6, "addition")
    reducer(4, 6, "subtraction")