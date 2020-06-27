#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
单例模式
控制对象创建过程的控制权
"""
class SingletonObject(object):
    class __SingleObject():
        """
        私有类，只有其外部类能够将其实例化
        """
        def __init__(self):
            self.val = None

        def __str__(self):
            return "{0!r} {1}".format(self, self.val)

        # the rest of the class definition will folow here, as per the previous logging script 
    instance = None

    def __new__(cls):
        if not SingletonObject.instance:
            SingletonObject.instance = SingletonObject.__SingleObject()
        return SingletonObject.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)