#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class MyList(object):
    """
    迭代器模式的Python内部实现
    Python定义了一个迭代器协议，用于创建可迭代对象并且之后可以返回一些知道如何遍历这些可迭代对象的对象
    Python使用了两个特定的方法调用以及一个封装好的异常来提供该语言环境下的迭代器功能。
    __iter__() 返回一个迭代器独享，该迭代器对象必须提供 __next__() 方法
    最后在遍历完所有元素之后，该迭代器会发出一个 StopIteration
    """
    def __init__(self, *args):
        self.list = list(args)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.index += 1
            return self.list[self.index -1]
        except IndexError as e:
            raise StopIteration()

if __name__ == "__main__":
    my_list = MyList(1, 2, 3, 4, 5, 6, 7)
    for i in my_list:
        print(i)