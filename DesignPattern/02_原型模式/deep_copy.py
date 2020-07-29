#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
python 深拷贝和浅拷贝示例

列表以及对象的浅拷贝原因
Python处理变量的方式与大家可能使用过的其他编程语言稍微有些不同。
除了基础类型，例如整数和字符串， Python中的变量更接近于标签或标记，而不是其他编程语言用作象征的存储桶。 
Python变量实际上是指向相关值在内存中存储位置的指针。
"""

# python引用，列表
a = list(range(1, 6))
print("[a] {}".format(a))
b = a
print("[b] {}".format(b))
b.append(6)
print("[a] {}".format(a))
print("[b] {}".format(b))

# 使用切片 浅拷贝列表
# 在处理浅列表时（仅包含实际值的列表，没有引用其他的复杂对象，例如列表或词典），切片运算符将完美地工作。
list_a = list(range(1, 6))
print("[list_a] {}".format(list_a))
list_b = list_a[:]
print("[list_b] {}".format(list_b))
list_b.append(6)
print("[list_a] {}".format(list_a))
print("[list_b] {}".format(list_b))

# 嵌套结构
lst1 = ['a', 'b', ['ab', 'ba']]
lst2 = lst1[:]
lst2[2][1] = 'd'
print("[lst1] {}".format(lst1))
print("[lst2] {}".format(lst2))

# 深拷贝 - 对任意列表进行完整的深拷贝
from copy import deepcopy
deep_lst1 = ['a', 'b', ['ab', 'ba']]
deep_lst2 = deepcopy(deep_lst1)
deep_lst2[2][1] = 'd'
print("[deep_lst1] {}".format(deep_lst1))
print("[deep_lst2] {}".format(deep_lst2))