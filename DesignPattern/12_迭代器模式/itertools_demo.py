#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
itertools 包使用演示
"""
from itertools import chain, cycle, zip_longest
from threading import Timer
import signal
from contextlib import contextmanager

def chain_demo():
    """
    chain() 函数   
    遍历迭代对象中的每一个值，并且将之全部转换成要被打印出来的单一列表
    """
    l = chain([1, 2, 3, 4], range(5, 6), "the quick and the slow")
    print(list(l))

def cycle_demo():
    """
    允许创建一个保持无限云鬟遍历传递给它的元素的迭代器。
    每次该循环器触及最后一个元素时，都会直接回到开始处重新开始。 
    """
    cycler = cycle([1, 2, 3])
    for x in cycler:
        print(x)

def zip_longest_demo():
    """
    合并一组可迭代对象并且在每一次迭代时返回他们匹配到的元素
    """
    list1 = [1, 2, 3]
    list2 = ['a', 'b', 'c']
    zipped = zip_longest(list1, list2)
    print(list(zipped))

if __name__ == "__main__":
    chain_demo()
    # cycle_demo()
    zip_longest_demo()