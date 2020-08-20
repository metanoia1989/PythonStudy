#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
模板方法模式的简单实现
"""

from abc import ABCMeta, abstractmethod

class TemplateAbstractBaseClass(metaclass=ABCMeta):
    def template_method(self):
        self._step_1()
        self._step_2()
        self._step_3()

    @abstractmethod
    def _step_1(self):
        pass

    @abstractmethod
    def _step_2(self):
        pass

    @abstractmethod
    def _step_3(self):
        pass

class ConcreteImplementationClass(TemplateAbstractBaseClass):
    def _step_1(self):
        pass

    def _step_2(self):
        pass

    def _step_3(self):
        pass