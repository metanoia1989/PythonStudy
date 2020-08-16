#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成器是简化迭代器创建的绝佳形式，生成器是一个函数，会生成一系列的结果，并且遵循Python迭代器协议接口。
在调用生成器函数时，会返回一个生成器对象，只有在首次调用`__next__()`方法时才会开始所有的执行。
"""


def gen_squares(n):
    i = 0
    while i < n:
        yield i * i
        print("next i")
        i += 1

if __name__ == "__main__":
    g = gen_squares(4)
    print(g)
    for i in g:
        print(i)

    # 生成器简写
    g = (x * x for x in range(4))
    print(g)
    # 生成器作为函数参数
    print(max(x * x for x in range(4)))