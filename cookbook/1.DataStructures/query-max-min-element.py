#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
从一个集合中获得最大或者最小的 N 个元素列表
heapq 模块有两个函数：nlargest() 和 nsmallest()
"""

import heapq

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
max_nums = heapq.nlargest(3, nums)
min_nums = heapq.nsmallest(3, nums)
print('*' * 20)
print("n larges nums {}".format(max_nums))
print("n smalls nums {}".format(min_nums))
print('*' * 20)

"""两个函数都能接受一个关键字参数，用于更复杂的数据结构"""
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65},
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
print('*' * 20)
print("cheap price {}".format(cheap))
print("expensive price {}".format(expensive))
print('*' * 20)

"""
在一个集合中查找最小或最大的 N 个元素，并且 N 小于集合元素数量
使用heapq.heapify 将集合数据进行堆排序后放入一个列表
堆数据结构最重要的特征是 heap[0] 永远是最小的元素。
heapq.heappop() 方法 将第一个元素弹出来，然后用下一个最小的元素来取代被弹出元素
（这种操作时间复杂度仅仅是 O(log N)，N 是堆大小）
"""
heap = list(nums)
heapq.heapify(heap)
print('*' * 20)
print('heap堆排序之后 {}'.format(heap))
print('heap弹出第一个元素 {}'.format(heapq.heappop(heap)))
print('heap弹出第一个元素 {}'.format(heapq.heappop(heap)))
print('heap弹出第一个元素 {}'.format(heapq.heappop(heap)))
print('*' * 20)