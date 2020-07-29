#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
原型模式的核心就是一个clone()函数，这个函数接收一个对象作为输入参数并且会返回它的一个副本。

一个原型模式实现的框架应该声明一个抽象基类，这个基类会指定一个纯虚方法 clone。
任何需要多态构造函数能力的类（这个类会根据它在实例化时所接收到的参数数量来决定使用
哪个构造函数都会从该抽象类派生其本身，并且实现这个 clone()方法。
每个单位都需要从这个抽象基类派生本身相较于编写在硬编码类名称上调用这个新运算符的代码，
客户端只要调用原型上的 clone 方法即可。
"""

from abc import ABCMeta, abstractmethod

class Prototype(metaclass=ABCMeta):
    @abstractmethod
    def clone(self):
        pass