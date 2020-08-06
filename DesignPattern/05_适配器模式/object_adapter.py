#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
相较于使用继承来封装一个类，我们可以使用组合的方式。
这样的话，适配 性来器就可以包含它所封装的类，
并且对所封装对象的实例进行调用。这个方法会进一步降低实现的复杂性。
"""

class InterfaceSuperClass(object):
        pass

class ObjectAdapter(IntefaceSuperClass):
    def __init__(self, what_i_have):
        self.what_i_have = what_i_have

    def required_function(self):
        return self.what_i_have.provided_function_1() 

    def __getattr__(self, attr):
        return getattr(self.what_i_have, attr) 