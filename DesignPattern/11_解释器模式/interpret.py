#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
每个类都有一个 interpret 方法，还需要一个类和对象来存储全局上下文对象。
这一上下文会被传递给解释流中下一个对象的interpret函数。
"""

class NoTerminal(object):
    def __init__(self, expression):
        self.expression = expression

    def interpret(self):
        self.expression.interpret()

class Terminal(object):
    def interpret(self):
        pass