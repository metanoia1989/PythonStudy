#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
访问者模式原型
"""

from abc import ABCMeta, abstractmethod

class Visitable(object):
    def accept(self, visitor):
        visitor.visit(self)

class CompositeVisitable(Visitable):
    def __init__(self, iterable):
        self.iterable = iterable

    def accept(self, visitor):
        for element in self.iterable:
            element.accept(visitor)
        visitor.visit(self)

class AbstractVisitor(object, metaclass=ABCMeta):
    @abstractmethod
    def visit(self, element):
        raise NotImplementedError("A visitor needs to define a visit method")

class ConcreteVisitable(Visitable):
    def __init__(self):
        pass

class ConcreteVisitor(AbstractVisitor):
    def visit(self, element):
        pass