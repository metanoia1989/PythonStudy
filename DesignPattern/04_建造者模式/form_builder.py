#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
建造者模式的实现
"""
from abc import ABCMeta, abstractmethod

class Director(object, metaclass=ABCMeta):
    def __init__(self):
        self._builder = None

    @abstractmethod
    def construct(self):
        pass

def get_constructed_object(self):
    return self._builder.constructed_object

class Builder(object, metaclass=ABCMeta):
    def __init__(self, constructed_object):
        self.constructed_object = constructed_object

class Product(object):
    def __init__(self):
        pass

    def __repr__(self):
        pass

class ConcreteBuilder(Builder):
    pass

class ConcreteDirector(Director):
    pass