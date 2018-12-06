#!/usr/bin/env python3
# -*- coding: utf-8  -*-

"""
一个包含 N 个元素的元组或者是序列，将它里面的值解压后同时赋值给 N 个变量        
任何的序列（或者是可迭代对象）可以通过一个简单的赋值语句解压并赋值给多个变量。
唯一的前提就是变量的数量必须跟序列元素的数量是一样的。
如果变量个数和序列元素的个数不匹配，会产生一个 ValueError 异常。
只想解压一部分，丢弃其他的值，使用任意变量名去占位，到时候丢掉这些变量就行了，常用`_`
"""

# 解压序列赋值
p = (4, 5)
x, y = p
print("{p} 解压赋值后: {x} {y}".format(p=p, x=x, y=y))

data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, date = data
print("{data} 解压赋值后: {name} {shares} {price} {date}".format(
    data=data, name=name, shares=shares, price=price, date=date
)) 

string = 'hello'
a, b, c, d, e = string
print("{string} 解压赋值后: {a} {b} {c} {d} {e}".format(
    string=string, a=a, b=b, c=c, d=d, e=e
))

ll = ['one', 'two', 'three']
_, two, _ = ll
print("{} 解压赋值后 {}".format(ll, two))

"""
一个可迭代对象的元素个数超过变量个数时，会抛出一个 ValueError
Python 的星号表达式，扩展的迭代解压语法是专门为解压不确定个数或任意个数元素的可迭代对象而设计的。
星号表达式在迭代元素为可变长元组的序列时是很有用的      
想解压一些元素后丢弃它们使用 *_, *ign
"""
# 解压可迭代对象

def drop_first_last(grades):
    """ 统计下家庭作业的平均成绩，但是排除掉第一个和最后一个分数 """
    first, *middle, last = grades
    return avg(middle)

"""分解用户记录"""
record = ('Dave', 'dave@example.com', '733-555-1212', '847-555-1212')
name, email, *phone_numbers = record
print("name是{}， email是{}, phone_number是: {}".format(name, email, phone_numbers))

"""一个公司前 8 个月销售数据, 对比最近一个月数据和前面 7 个月的平均值"""
sales_record = [123, 221, 352, 141, 251, 981, 435, 111, 566]
def compare_last_month_three_avg(sales_record):
    *trailing_qtrs, current_qtr = sales_record
    trailing_avg = sum(trailing_qtrs) / len(trailing_qtrs)
    return current_qtr > trailing_avg 

"""用星号表达式迭代元素为可变长元组的序列"""
records = [
    ('foo', 1, 2),
    ('bar', 'hello'),
    ('foo', 3, 4)
]

def do_foo(x, y):
    print('foo', x, y)

def do_bar(s):
    print('bar', s)

for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)
