#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
实现一个按优先级排序的队列，在这个队列上面每次 pop 操作总是返回优先级最高的那个元素
"""

import heapq

class PriorityQueue():
    """
    函数 heapq.heappush() 和 heapq.heappop() 分别在队列 _queue 上插入和删除第一个元素， 
    并且队列 _queue 保证第一个元素拥有最高优先级
    由于 push 和 pop 操作时间复杂度为 O(log N)，其中 N 是堆的大小，因此就算是 N 很大的时候它们运行速度也依旧很快。
    在多个线程中使用同一个队列，那么你需要增加适当的锁和信号量机制
    """
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1
    
    def pop(self):
        return heapq.heappop(self._queue)[-1]


class Item:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return 'Item({!r})'.format(self.name)
    

"""
如果两个有着相同优先级的元素（ foo 和 grok ），pop 操作按照它们被插入到队列的顺序返回的。
"""    
queue = PriorityQueue()
queue.push(Item('foo'), 1)
queue.push(Item('bar'), 5)
queue.push(Item('spam'), 4)
queue.push(Item('grok'), 1)
print('#' * 20)
print('弹出一个优先级最高的元素 {}'.format(queue.pop()))
print('弹出一个优先级最高的元素 {}'.format(queue.pop()))
print('弹出一个优先级最高的元素 {}'.format(queue.pop()))
print('弹出一个优先级最高的元素 {}'.format(queue.pop()))
print('#' * 20)