#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
迭代操作只保留最后有限几个元素的历史记录
使用 collections.deque 
"""

from collections import deque
from os.path import dirname

def search(lines, pattern, history=5):
    """
    在多行上面做简单的文本匹配， 并返回匹配所在行的最后N行
    :line 搜索的行
    :pattern 需要匹配行的标识
    :history 要取出的数量
    """
    previous_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)
    
with open(dirname(__file__) + './historyfile.txt') as f:
    for line, prevlines in search(f, 'python', 5):
        for pline in prevlines:
            print(pline, end='')
        print(line, end='')
        print('-' * 20)

"""
使用 deque(maxlen=N) 构造函数会新建一个固定大小的队列。
当新的元素加入并且这个队列已满的时候， 最老的元素会自动被移除掉。
可以手动在一个列表上实现这一的操作，使用队列变得更简单。
不设置最大队列大小，那么就会得到一个无限大小队列，可以在队列的两端执行添加和弹出元素的操作。
在队列两端插入或删除元素时间复杂度都是 O(1) ，区别于列表，在列表的开头插入或删除元素的时间复杂度为 O(N)
"""

print('*' * 20)
q = deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)
print("q is {}".format(q))
q.append(4)
print("q is {}".format(q))
q.append(5)
print("q is {}".format(q))

print('*' * 20)
infiniteQ = deque()
infiniteQ.append(1)
infiniteQ.append(2)
infiniteQ.append(3)
print("infiniteQ is {}".format(infiniteQ))
infiniteQ.appendleft(4)
print("infiniteQ is {}".format(infiniteQ))
infiniteQ.pop()
print("infiniteQ is {}".format(infiniteQ))
infiniteQ.popleft()
print("infiniteQ is {}".format(infiniteQ))
print('*' * 20)